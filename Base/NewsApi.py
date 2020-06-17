import requests
import json
from bs4 import BeautifulSoup


def getNews(category):
    newsDictionary = []

    try:
        if category != 'all':
            htmlBody = requests.get('https://www.inshorts.com/en/read/' + category)
        else:
            htmlBody = requests.get('https://www.inshorts.com/en/read/')

    except requests.exceptions.RequestException as e:
        newsDictionary.append(str(e.message))
        return newsDictionary

    soup = BeautifulSoup(htmlBody.text, 'html5lib')
    newsCards = soup.find_all(class_='news-card')

    for index, card in enumerate(newsCards):

        try:
            readMoreUrl = card.find(class_='read-more').find('a').get('href')
            if str(readMoreUrl).startswith('https://ad.doubleclick.net/'):
                continue
        except AttributeError:
            readMoreUrl = 'None'

        try:
            title = card.find(class_='news-card-title').find('a').text
        except AttributeError:
            title = None

        # try:
        #     imageUrl = card.find(
        #         class_='news-card-image')['style'].split("'")[1]
        # except AttributeError:
        #     imageUrl = None

        try:
            url = ('https://www.inshorts.com' + card.find(class_='news-card-title')
                   .find('a').get('href'))
        except AttributeError:
            url = None

        try:
            content = card.find(class_='news-card-content').find('div').text
            # content = '\n'.join(content.split(". "))
        except AttributeError:
            content = None

        # try:
        #     author = card.find(class_='author').text
        # except AttributeError:
        #     author = None

        try:
            date = card.find(clas='date').text
        except AttributeError:
            date = None

        try:
            time = card.find(class_='time').text
        except AttributeError:
            time = None

        newsObject = {
            'title': str(title).strip(),
            # 'imageUrl': imageUrl,
            'url': url,
            'content': content,
            # 'author': author,
            'date': date,
            'time': time,
            'readMoreUrl': readMoreUrl
        }

        newsDictionary.append(newsObject)

    return json.dumps(newsDictionary)
