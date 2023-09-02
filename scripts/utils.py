import zipfile
from healthkit_to_sqlite.cli import cli as healthKitDB
import sqlite_utils
from healthkit_to_sqlite.utils import *
from pathlib import Path
import sqlite3
import os
import requests
import pytz
from datetime import datetime, timedelta

zip_path = Path('data/экспорт.zip')
db_path = Path('data/healthkit.db')

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

def parseHealthData():
    exportHealthKitData(zip_path, db_path)

    db = sqlite3.connect(Path('data/healthkit.db'))
    cursor = db.cursor()
    cursor.execute("""
                SELECT workoutActivityType, duration, durationUnit, startDate, endDate FROM workouts
                """)
    result = cursor.fetchall()
    cursor.execute("""
                SELECT value, creationDate, sourceName FROM rStepCount
                """)
    steps = cursor.fetchall()
    cursor.execute("""
                SELECT dateComponents, activeEnergyBurned FROM activity_summary
                """)
    calories = cursor.fetchall()
    cursor.execute("""
                SELECT value FROM rVO2Max
                """)
    rvo2max = cursor.fetchall()
    db.close()
    rvo2max = rvo2max[-1][0]

    utc=pytz.utc


    parsedWorkouts = []
    days = set()
    yogaMinutes = 0
    runMinutes = 0
    for element in result:
        if datetime.strptime(element[3], '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=utc) >= (datetime.now() - timedelta(days=7)).replace(tzinfo=utc):
            if element[0] == 'HKWorkoutActivityTypeYoga':
                yogaMinutes = yogaMinutes + float(element[1])
            if element[0] == 'HKWorkoutActivityTypeRunning':
                runMinutes = runMinutes + float(element[1])
            runMinutes = round(runMinutes)
            yogaMinutes = round(yogaMinutes)
                    
    stepSum = 0
    for step in steps:
        if datetime.strptime(step[1], '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=utc) >= (datetime.now() - timedelta(days=7)).replace(tzinfo=utc) and step[2] == 'Apple Watch — Владислав':
            stepSum = stepSum + int(step[0])
            days.add(datetime.strptime(step[1], '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=utc).date())
            
    calSum = 0
    for calorie in calories:
        if datetime.strptime(calorie[0], '%Y-%m-%d') >= (datetime.now() - timedelta(days=7)):
            calSum = calSum + float(calorie[1])
        calSum = round(calSum)

    print('HealthKit data parsed succesefully.')
    return stepSum, calSum, yogaMinutes, runMinutes, rvo2max


def timeCong(number, time):
    numgroups = (0, 5, 6, 7, 8, 9), [1], (2, 3, 4)
    conjgs = {
            'minutes': ('минут', 'минуту', 'минуты'),
            'hours': ('часов', 'час', 'часа'),
            'seconds': ('секунд', 'секунда', 'секунды')
            }
    con = list(zip(numgroups, conjgs[time]))
    if int(repr(number)[-2]) == 1:
        return con[0][1]
    last_digit = int(repr(number)[-1])
    for group in con:
        if last_digit in group[0]:
            return group[1]



