import requests
import time
from bs4 import BeautifulSoup

def getLivelibRecent(user):
    global banned
    global page
    page = 1
    banned = False
    readlist = []
    liveLibURL = f'https://www.livelib.ru/reader/{user}/read/'
    text = requests.get(liveLibURL)
    parsedtext = BeautifulSoup(text.content, "html.parser")

    titles = parsedtext.findAll('a', class_="brow-book-name with-cycle")
    authors = parsedtext.findAll('a', class_="brow-book-author")
    isListEmpty = parsedtext.find('p', string='Этот список пока пуст.')

    for i in range(len(titles)):
        tit = titles[i].text
        aut = authors[i].text
        book = {'title': tit, 'author': aut}
        readlist.append(book)

    if parsedtext.find('form', action="/service/ratelimitcaptcha") is not None:
        banned = True
        print('Слишком много запросов')

    if len(readlist) >= 20 and banned == False:
        time.sleep(10)
        print('list is longer', isListEmpty)
        page = 2
        while isListEmpty == None and banned == False:
            print('list is empty')
            text = requests.get(liveLibURL+"~"+str(page))
            titles = parsedtext.findAll('a', class_="brow-book-name with-cycle")
            authors = parsedtext.findAll('a', class_="brow-book-author")
            isListEmpty = parsedtext.find('p', string='Этот список пока пуст.')
            if parsedtext.find('form', action="/service/ratelimitcaptcha") is not None:
                banned = True
                print('Слишком много запросов')
            
            print(isListEmpty)

            for i in range(len(titles)):
                tit = titles[i].text
                aut = authors[i].text
                book = {'title': tit, 'author': aut}
                readlist.append(book)
            
            page += 1
            time.sleep(10)

    return readlist

# Вариант если удастся обойти капчу livelib
def getReadListAll(user):
    global banned
    global page
    page = 1
    banned = False
    readlist = []
    liveLibURL = f'https://www.livelib.ru/reader/{user}/read/'
    text = requests.get(liveLibURL)
    parsedtext = BeautifulSoup(text.content, "html.parser")

    titles = parsedtext.findAll('a', class_="brow-book-name with-cycle")
    authors = parsedtext.findAll('a', class_="brow-book-author")
    isListEmpty = parsedtext.find('p', string='Этот список пока пуст.')

    for i in range(len(titles)):
        tit = titles[i].text
        aut = authors[i].text
        book = {'title': tit, 'author': aut}
        readlist.append(book)

    if parsedtext.find('form', action="/service/ratelimitcaptcha") is not None:
        banned = True
        print('Слишком много запросов')

    if len(readlist) >= 20 and banned == False:
        time.sleep(10)
        print('list is longer', isListEmpty)
        page = 2
        while isListEmpty == None and banned == False:
            print('list is empty')
            text = requests.get(liveLibURL+"~"+str(page))
            titles = parsedtext.findAll('a', class_="brow-book-name with-cycle")
            authors = parsedtext.findAll('a', class_="brow-book-author")
            isListEmpty = parsedtext.find('p', string='Этот список пока пуст.')
            if parsedtext.find('form', action="/service/ratelimitcaptcha") is not None:
                banned = True
                print('Слишком много запросов')
            
            print(isListEmpty)

            for i in range(len(titles)):
                tit = titles[i].text
                aut = authors[i].text
                book = {'title': tit, 'author': aut}
                readlist.append(book)
            
            page += 1
            time.sleep(10)

    return readlist
