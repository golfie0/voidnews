from django.shortcuts import render
from bs4 import BeautifulSoup
import requests  # библиотека для http запросов
import re  # регулярные выражения
import time
import threading

habr = 'https://habr.com/ru/news/'
dnews = 'https://3dnews.ru/editorial'
hinews = 'https://hi-news.ru/'
four_pda = 'https://4pda.ru/games/'

habr_list = []
img_list = []
title_list = []
url_list = []


def get_habr():
    req = requests.get(habr).text
    soup = BeautifulSoup(req, 'lxml')
    posts = soup.find_all('article', class_='post post_preview')
    images = soup.find_all("img")
    for img in images:
        src = img.get("src")
        if src != None:
            src = re.sub('https://habrastorage\.org/getpro/moikrug/\S+', '', src)
            src = re.findall('https://habrastorage\.org/\S+', src)
            src = "".join(src)
            if src != '':
                img_list.append(src)

    for post in posts:
        title = post.find('h2', class_='post__title').text
        title = re.sub('\\n', '', title)
        title.replace('\xa0', ' ')
        url = post.find('a', class_='post__title_link').get('href')
        url = "".join(url)
        if url != "":
            title_list.append(title)
            url_list.append(url)

    for i in range(0, len(img_list) - 1):
        data = {
            'title': title_list[i],
            'url': url_list[i],
            'image': img_list[i],
        }
        habr_list.append(data)
    time.sleep(300)
    get_habr()


thread = threading.Thread(target=get_habr)
thread.start()


def home(req):
    context = {
        'habr_list': habr_list,
    }
    return render(req, 'news_app/home.html', context)
