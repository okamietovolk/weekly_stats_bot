from scripts import keydata
from scripts.parsers import *
from pathlib import(Path)
import json
import datetime


today = datetime.date.today()
weekBefore = today - datetime.timedelta(days=6)
week = f'{today.strftime("%d/%m")} - {weekBefore.strftime("%d/%m") } {today.strftime("%Y")}'
 

combolist = {'bookmate': getBookmateFinished(keydata.bookmateLogin), 'letterboxd': getLetterboxdRecent(keydata.letterboxdLogin)}

def getStats():
    with open(Path('data/saved.json')) as fp:
        old = json.load(fp)

    social = keydata.social
    diff = {'bookmate': [], 'letterboxd': []}

    for soc in social:
        for element in combolist[soc]:
            if element not in old[soc]:
                diff[soc].append(element) 
            # if old[soc]:
            #      with open(Path('data/saved.json'), 'w+') as f:
            #          json.dump(combolist, f)

    # Dump commented
    with open(Path('data/diff.json'), 'w+') as f:
        json.dump(diff, f)

    print(diff)
    output = f'✨⭐️Автоматическая недельная статистика!⭐️✨\n\n📆 Неделя {week}\n\n'

    for soc in social:

        if diff[soc]:
            
            if soc == 'letterboxd':
                
                    output = output + '🍿 На этой неделе просмотрено:\n'
                    for entry in diff[soc]:
                        output = output + f'🎥 <a href=\"{entry["link"]}\">{entry["title"]}</a> - {entry["raiting"]}\n'
                        
            elif soc == 'bookmate':
                
                    currentReading = getBookmateCurrent(keydata.bookmateLogin)
                    if currentReading:
                        output = output + '📖 Сейчас читаю:\n'
                        for entry in currentReading:
                            output = output + f'📜 <a href=\"{entry["link"]}\">{entry["title"]}</a> - {entry["author"]} 📜\n'
                        output = output + '\n'

                    output = output + '📚 На этой неделе дочитал:\n'
                    bookemojis = ['📕', '📗', '📘', '📙']
                    i = 0
                    for entry in diff[soc]:
                        output = output + f'{bookemojis[i]} <a href=\"{entry["link"]}\">{entry["title"]}</a> - {entry["author"]} {bookemojis[i]}\n'
                        i = (i + 1) % len(bookemojis)

            output = output + '\n\n'

    workouts = getWorkouts()
    if workouts['bestTime'] != timedelta():
        km5message = f'🏃Лучшее время на 5 км: {workouts["bestTime"]}\n'
    output = output + f'🏃🏻‍♂️ Пробежал: {round(workouts["distance"], 2)} км\n{km5message}🧘🏼 Занимался йогой: {workouts["yogaHours"]} часа {workouts["yogaMinutes"]} минут'
    
    weekTrack = getLastFMtopTrack7(keydata.lastFMlogin)
    if weekTrack:
        output = output + f'\n\n🎹 Трек недели:\n<a href=\"{weekTrack["link"]}\">{weekTrack["title"]}</a> - {weekTrack["artist"]}'
            
    return output