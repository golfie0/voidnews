import requests
from bs4 import BeautifulSoup
import requests  # библиотека для http запросов
import datetime
import re
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.shortcuts import render
from .models import Posts

tproger_links = []
tproger_titles = []


def add_news(table, title, link):
    images = {
        'habr': 'https://www.google.com/s2/favicons?domain=habr.com',
        'dnews': 'https://www.google.com/s2/favicons?domain=3dnews.ru',
        'tproger': 'https://www.google.com/s2/favicons?domain=tproger.ru',
    }
    title = re.sub('"', '', title)
    title = re.sub("'", '', title)
    try:
        post = Posts.objects.create(title=title, source=link,
                                    date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), img=images.get(table))
        post.save(force_insert=True)
    except IntegrityError:
        pass


def get_habr1():  # парс на один раз для заполнения бд
    for i in reversed(range(1, 31)):
        habr = 'https://habr.com/ru/news/page{}/'.format(i)
        req = requests.get(habr).text
        soup = BeautifulSoup(req, 'lxml')
        posts = soup.find_all('a', class_='post__title_link')
        for title in posts:
            habr_link = title.get('href')
            habr_title = title.get_text()
            add_news('habr', habr_title, habr_link)


def get_habr():
    habr = 'https://habr.com/ru/news/'
    req = requests.get(habr).text
    soup = BeautifulSoup(req, 'lxml')
    posts = soup.find_all('a', class_='post__title_link')
    for title in posts:
        habr_link = title.get('href')
        habr_title = title.get_text()
        add_news('habr', habr_title, habr_link)


def get_tproger():
    global tproger_titles
    global tproger_links
    tproger = 'https://tproger.ru/news/'
    req = requests.get(tproger).text
    soup = BeautifulSoup(req, 'lxml')
    posts = soup.find_all('a', class_='article-link')
    for link in posts:
        tproger_links.append(link.get('href'))
    posts = soup.find_all('h2', class_='entry-title')
    for title in posts:
        tproger_titles.append(title.get_text('h2'))
    for i in range(0, len(tproger_titles)):
        add_news('tproger', tproger_titles[i], tproger_links[i])


def get_tproger1():
    global tproger_titles
    for i in reversed(range(1, 100)):
        tproger = 'https://tproger.ru/news/page/{}/'.format(i)
        req = requests.get(tproger).text
        soup = BeautifulSoup(req, 'lxml')
        posts = soup.find_all('a', class_='article-link')
        for link in posts:
            tproger_links.append(link.get('href'))
        posts = soup.find_all('h2', class_='entry-title')
        for title in posts:
            tproger_titles.append(title.get_text('h2'))
        tproger_titles = [re.sub("'", '', i) for i in tproger_titles]
        tproger_titles = [re.sub('"', '', i) for i in tproger_titles]
    for i in range(0, len(tproger_titles)):
        add_news('tproger', tproger_titles[i], tproger_links[i])


def get_dnews():
    dnews = 'https://3dnews.ru/news/'
    req = requests.get(dnews).text
    soup = BeautifulSoup(req, 'lxml')
    posts = soup.find_all('a', class_='entry-header')
    for title in posts:
        dnews_title = title.get_text('h1')
        dnews_link = title.get('href')
        dnews_link = 'https://3dnews.ru/' + dnews_link
        add_news('dnews', dnews_title, dnews_link)


def get_dnews1():
    for i in reversed(range(1, 101)):
        dnews = 'https://3dnews.ru/news/page-{}.html'.format(i)
        req = requests.get(dnews).text
        soup = BeautifulSoup(req, 'lxml')
        posts = soup.find_all('a', class_='entry-header')
        for title in posts:
            dnews_title = title.get_text('h1')
            dnews_link = title.get('href')
            dnews_link = 'https://3dnews.ru/' + dnews_link
            add_news('dnews', dnews_title, dnews_link)


def home(req):
    test = req.GET['array']
    logging.info(test)
    news_list = Posts.objects.order_by('-date')

    paginator = Paginator(news_list, 40)
    page = req.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    def title_check():
        for new in news:
            if len(new.title) >= 100:
                new.title = (new.title[:97] + '..')

    title_check()
    if req.GET.get('refresh'):
        get_habr()
        get_dnews()
        get_tproger()

    context = {
        'news_list': news_list,
        'news': news,
        'page': page,
    }
    return render(req, 'news_app/home.html', context)
