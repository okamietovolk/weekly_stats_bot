import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import zipfile, sqlite_utils, sqlite3, pytz
from healthkit_to_sqlite.utils import *
from pathlib import Path
from datetime import datetime, timedelta

lastFMuserURL = "https://www.last.fm/user/"
lastFMtracks = "/library/tracks"

class bookmate:
    def __init__(self, username) -> None:
        self.user = username
        self.current = BeautifulSoup(requests.get('https://bookmate.ru/'+self.user+"/books/recent").content, "html.parser")
        self.finished = BeautifulSoup(requests.get('https://bookmate.ru/'+self.user+"/books/finished").content, "html.parser")
        
    def getCurrent(self):
        '''
        Returns recent bookmate current entries (reading)

        Args:
            username (str): letterboxd username

        Returns:
            list: a list of dictionaries: {'title': book title, 'author': author}
        '''

        titles = self.current.findAll('a', class_="book__title")
        authors = self.current.findAll('span', class_="authors-list")
        readlist = []

        for i in range(len(titles)):
            title = titles[i].text
            author = authors[i].text
            link = f'https://bookmate.ru{titles[i]["href"]}'
            book = {'title': title, 'author': author, 'link': link}
            readlist.append(book)

        return readlist

    def getFinished(self):
        '''
        Returns recent bookmate finished entries

        Args:
            username (str): letterboxd username

        Returns:
            list: a list of dictionaries: {'title': book title, 'author': author}
        '''
        titles = self.finished.findAll('a', class_="book__title")
        authors = self.finished.findAll('span', class_="authors-list")
        readlist = []

        for i in range(len(titles)):
            title = titles[i].text
            author = authors[i].text
            link = f'https://bookmate.ru{titles[i]["href"]}'
            book = {'title': title, 'author': author, 'link': link}
            readlist.append(book)

        return readlist
    
class letterboxd:
    
    def __init__(self, username) -> None:
        self.user = username
        self.movies = BeautifulSoup(requests.get("https://letterboxd.com/"+self.user+"/films/diary/").text, "html.parser").findAll('tr', class_="diary-entry-row")
        
    def getRecent(self):

        """
        Returns last 50 letterboxd entries

        Args:
            username (str): letterboxd username

        Returns:
            list: a list of dictionaries: {'title': movie title, 'raiting': user's raiting, 'liked': heart if liked}
        """
        
        list = []
        
        for movie in self.movies:
            heads = movie.find('h3').text
            stars = movie.find('div', class_="hide-for-owner").text
            like = movie.find('span', class_="has-icon icon-16 large-liked icon-liked hide-for-owner")
            link = movie.find('td', class_="td-film-details")
            link = link.find('div', class_='film-poster')
            link = f'https://letterboxd.com/film/{link.get("data-film-slug")}/'
            # moviehtml= requests.get(link).text
            # moviehtml = BeautifulSoup(moviehtml, "html.parser")
            # director = moviehtml.findall('a', href="/director/contributor*").text
            if like != None:
                heart = "❤️"
            else:
                heart = ""

            list.append({'title': heads, 'raiting': stars, 'liked': heart, 'link': link})

        return list
    
class healthData:
    
    def exportHealthKitData(export_zip, db_path):
        
        if db_path.is_file():
            db_path.unlink()
        zf = zipfile.ZipFile(export_zip)
        filenames = {zi.filename for zi in zf.filelist}
        export_xml_path = None
        for filename in filenames:
            if filename.count("/") == 1 and filename.endswith(".xml"):
                firstbytes = zf.open(filename).read(1024)
                if (
                    b"<!DOCTYPE HealthData" in firstbytes
                    or b"<HealthData " in firstbytes
                ):
                    export_xml_path = filename
                    break
        fp = zf.open(export_xml_path)
        file_length = zf.getinfo(export_xml_path).file_size
        db = sqlite_utils.Database(db_path)
        convert_xml_to_sqlite(fp, db, zipfile=zf)
        print('Healthkit data exported succesefully.')
    
    def __init__(self, zip_path, db_path) -> None:
        
        self.exportHealthKitData(zip_path, db_path)

        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        cursor.execute("""
                    SELECT workoutActivityType, duration, durationUnit, startDate, endDate FROM workouts
                    """)
        self.result = cursor.fetchall()
        cursor.execute("""
                    SELECT value, creationDate, sourceName FROM rStepCount
                    """)
        self.steps = cursor.fetchall()
        cursor.execute("""
                    SELECT dateComponents, activeEnergyBurned FROM activity_summary
                    """)
        self.calories = cursor.fetchall()
        cursor.execute("""
                    SELECT value FROM rVO2Max
                    """)
        rvo2max = cursor.fetchall()
        db.close()
        self.rvo2max = rvo2max[-1][0]
        self.utc=pytz.utc
        
    def weeklyCalories(self):
        calSum = 0
        for calorie in self.calories:
            if datetime.strptime(calorie[0], '%Y-%m-%d') >= (datetime.now() - timedelta(days=7)):
                calSum = calSum + float(calorie[1])
            calSum = round(calSum)
        return calSum
        
    def weeklySteps(self):
        stepSum = 0
        days = set()
        for step in self.steps:
            if datetime.strptime(step[1], '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=self.utc) >= (datetime.now() - timedelta(days=7)).replace(tzinfo=self.utc) and step[2] == 'Apple Watch — Владислав':
                stepSum = stepSum + int(step[0])
                days.add(datetime.strptime(step[1], '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=self.utc).date())
        return stepSum
                
    def workoutTime(self):
        yogaMinutes = 0
        runMinutes = 0
        for element in self.result:
            if datetime.strptime(element[3], '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=self.utc) >= (datetime.now() - timedelta(days=7)).replace(tzinfo=self.utc):
                if element[0] == 'HKWorkoutActivityTypeYoga':
                    yogaMinutes = yogaMinutes + float(element[1])
                if element[0] == 'HKWorkoutActivityTypeRunning':
                    runMinutes = runMinutes + float(element[1])
                runMinutes = round(runMinutes)
                yogaMinutes = round(yogaMinutes)
        return yogaMinutes, runMinutes

def getLastFMtopTrack7(username):
    url = lastFMuserURL + username
    html = requests.get(url, params='date_preset=LAST_7_DAYS')
    html = BeautifulSoup(html.content, "html.parser")
    topTrack = html.find('section', id="top-tracks")
    title = topTrack.find('td', class_="chartlist-name").find('a')
    artist = topTrack.find('td', class_="chartlist-artist").find('a')
    return {'title': title.text, 'artist': artist.text, 'link': f'https://www.last.fm{title.get("href")}'}
