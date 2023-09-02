import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
from datetime import datetime, timedelta
import pydrive

bookmateWeb = 'https://bookmate.ru/'
bookmateRecent = "/books/recent"
bookmateFinished = "/books/finished"
letterboxdWeb = "https://letterboxd.com/"
letterboxdDiary = "/films/diary/"
lastFMuserURL = "https://www.last.fm/user/"
lastFMtracks = "/library/tracks"


def getBookmateCurrent(username):
    '''
    Returns recent bookmate current entries (reading)

    Args:
        username (str): letterboxd username

    Returns:
        list: a list of dictionaries: {'title': book title, 'author': author}
    '''
    stats = requests.get(bookmateWeb+username+bookmateRecent)
    stats = BeautifulSoup(stats.content, "html.parser")

    titles = stats.findAll('a', class_="book__title")
    authors = stats.findAll('span', class_="authors-list")
    readlist = []

    for i in range(len(titles)):
        title = titles[i].text
        author = authors[i].text
        link = f'https://bookmate.ru{titles[i]["href"]}'
        book = {'title': title, 'author': author, 'link': link}
        readlist.append(book)

    return readlist

def getBookmateFinished(username):
    '''
    Returns recent bookmate finished entries

    Args:
        username (str): letterboxd username

    Returns:
        list: a list of dictionaries: {'title': book title, 'author': author}
    '''
    stats = requests.get(bookmateWeb+username+bookmateFinished)
    stats = BeautifulSoup(stats.content, "html.parser")

    titles = stats.findAll('a', class_="book__title")
    authors = stats.findAll('span', class_="authors-list")
    readlist = []

    for i in range(len(titles)):
        title = titles[i].text
        author = authors[i].text
        link = f'https://bookmate.ru{titles[i]["href"]}'
        book = {'title': title, 'author': author, 'link': link}
        readlist.append(book)

    return readlist

def getLetterboxdRecent(username):

    """
    Returns last 50 letterboxd entries

    Args:
        username (str): letterboxd username

    Returns:
        list: a list of dictionaries: {'title': movie title, 'raiting': user's raiting, 'liked': heart if liked}
    """
    html = requests.get(letterboxdWeb+username+letterboxdDiary).text
    html = BeautifulSoup(html, "html.parser")
    list = []
    movies = html.findAll('tr', class_="diary-entry-row")
    
    for movie in movies:
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

def getWorkouts():
    with open(Path('data/health.json'), 'r') as f:
        health = json.load(f)
    health = health['data']
    workouts = health['workouts']
    distance = 0
    bestTime5 = timedelta()
    bestTime10 = timedelta()
    yogahours = 0
    runs = [workout for workout in workouts if workout['name'] == 'Running']
    yogas = [workout for workout in workouts if workout['name'] == 'Yoga']
    for run in runs:
        distance = distance + run['distance']['qty']
        if int(round(run['distance']['qty'], 0)) == 5:
            time = datetime.strptime(run['end'], '%Y-%m-%d %H:%M:%S %z') - datetime.strptime(run['start'], '%Y-%m-%d %H:%M:%S %z')
            if time < bestTime5 or bestTime5 == timedelta():
                bestTime5 = time
                print(bestTime5)
        if int(round(run['distance']['qty'], 0)) == 10:
            time = datetime.strptime(run['end'], '%Y-%m-%d %H:%M:%S %z') - datetime.strptime(run['start'], '%Y-%m-%d %H:%M:%S %z')
            if time < bestTime10 or bestTime10 == timedelta():
                bestTime10 = time
        # тут данные епты
        runQ = len(runs)
        
    yogatotal = timedelta(minutes = 0)
    
    for yoga in yogas:
        yogatime = datetime.strptime(yoga['end'], '%Y-%m-%d %H:%M:%S %z') - datetime.strptime(yoga['start'], '%Y-%m-%d %H:%M:%S %z')
        yogatotal = yogatotal + yogatime
        
    total_seconds = yogatotal.total_seconds()
    yogaHours = int(total_seconds // 3600)
    yogaMinutes = int((total_seconds % 3600) // 60)
    
    return  {'distance': distance, 'bestTime5': bestTime5, 'bestTime10': bestTime10, 'yogaHours': yogaHours, 'yogaMinutes': yogaMinutes}

def getLastFMtopTrack7(username):
    url = lastFMuserURL + username
    html = requests.get(url, params='date_preset=LAST_7_DAYS')
    html = BeautifulSoup(html.content, "html.parser")
    topTrack = html.find('section', id="top-tracks")
    title = topTrack.find('td', class_="chartlist-name").find('a')
    artist = topTrack.find('td', class_="chartlist-artist").find('a')
    return {'title': title.text, 'artist': artist.text, 'link': f'https://www.last.fm{title.get("href")}'}