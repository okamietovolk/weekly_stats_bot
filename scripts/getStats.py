from scripts import keydata, server, utils
from scripts.parsers import *
from pathlib import(Path)
import json
import datetime


today = datetime.date.today()
weekBefore = today - datetime.timedelta(days=6)
week = f'{weekBefore.strftime("%d/%m")} - {today.strftime("%d/%m")} - {today.strftime("%Y")}'
 

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
                print(f'Found new element: {element}') 
            if old[soc]:
                 with open(Path('data/saved.json'), 'w+') as f:
                     json.dump(combolist, f)

    # Dump commented
    with open(Path('data/diff.json'), 'w+') as f:
        json.dump(diff, f)

    output = f'✨⭐️Автоматическая недельная статистика!⭐️✨\n\n📆 Неделя {week}\n\n'

    for soc in social:

        if diff[soc]:
            
            if soc == 'letterboxd':
                
                    output = output + '🍿 На этой неделе просмотрено:\n'
                    for entry in diff[soc]:
                        print(f'Added movie \"{entry["title"]}\" to the summary')
                        output = output + f'🎥 <a href=\"{entry["link"]}\">{entry["title"]}</a> - {entry["raiting"]}\n'
                        
            elif soc == 'bookmate':
                
                    output = output + '📚 На этой неделе дочитал:\n'
                    bookemojis = ['📕', '📗', '📘', '📙']
                    i = 0
                    for entry in diff[soc]:
                        print(f'Added book \"{entry["title"]}\" to the summary')
                        output = output + f'{bookemojis[i]} <a href=\"{entry["link"]}\">{entry["title"]}</a> - {entry["author"]} {bookemojis[i]}\n'
                        i = (i + 1) % len(bookemojis)

            output = output + '\n\n'

    currentReading = getBookmateCurrent(keydata.bookmateLogin)
    if currentReading:
        bookemojis = ['📔', '📓']
        output = output + '📖 Сейчас читаю:\n'
        i = 0
        for entry in currentReading:
            print(f'Added current book \"{entry["title"]}\" to the summary')
            output = output + f'{bookemojis[i]} <a href=\"{entry["link"]}\">{entry["title"]}</a> - {entry["author"]} {bookemojis[i]}\n'
            i = (i + 1) % len(bookemojis)
        output = output + '\n'
    
    stepSum, calSum, yogaMinutes, runMinutes, rvo2max = utils.parseHealthData()
    output = output + f'👣 Пройдено шагов за неделю: {stepSum}\n🔥 Сожжено калорий на тренировках: {calSum}\n\
🧘🏼 Занимался йогой: {yogaMinutes} {utils.timeCong(yogaMinutes, "minutes")}\n\
🏃 Бегал: {runMinutes} {utils.timeCong(runMinutes, "minutes")}\n\
❣️ Показатель <a href=\"https://ru.wikipedia.org/wiki/Максимальное_потребление_кислорода\">МПК</a>: {rvo2max}'
    

    weekTrack = getLastFMtopTrack7(keydata.lastFMlogin)
    if weekTrack:
        print(f"Top track {weekTrack['title']} added to the summary")
        output = output + f'\n\n🎹 Трек недели:\n🎶 <a href=\"{weekTrack["link"]}\">{weekTrack["title"]}</a> - {weekTrack["artist"]} 🎶'
            
    return output