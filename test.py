from bs4 import BeautifulSoup
import requests  # библиотека для http запросов
import psycopg2
import datetime
import re
from django.shortcuts import render

habr_links = []
habr_titles = []
tproger_links = []
tproger_titles = []
dnews_links = []
dnews_titles = []

connection = psycopg2.connect(user='postgres', password='root', host='localhost', port='5432')
cursor = connection.cursor()
connection.autocommit = True


def add_news(table, titles, links):
    for title in range(0, len(titles)):
        try:
            cursor.execute("""INSERT INTO news_app_post_{} (post_title, post_source, pub_date) VALUES ('{}', '{}', 
            '{}')""".format(table, titles[title],
                            links[title], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        except psycopg2.errors.UniqueViolation:
            pass
        except psycopg2.errors.InFailedSqlTransaction:
            pass
        except psycopg2.errors.StringDataRightTruncation:
            pass


def get_titles(table):
    cursor.execute("""SELECT post_title FROM news_app_post_{} ORDER BY id desc limit 20""".format(table))
    titles = [r[0] for r in cursor.fetchall()]
    return titles


def get_links(table):
    cursor.execute("SELECT post_source FROM news_app_post_{} ORDER BY id desc limit 20".format(table))
    links = [r[0] for r in cursor.fetchall()]
    return links


def get_habr1():  # парс на один раз для заполнения бд
    global habr_titles
    for i in reversed(range(1, 31)):
        habr = 'https://habr.com/ru/news/page{}/'.format(i)
        req = requests.get(habr).text
        soup = BeautifulSoup(req, 'lxml')
        posts = soup.find_all('a', class_='post__title_link')
        for link in posts:
            habr_links.append(link.get('href'))
            habr_titles.append(link.get_text())
        habr_titles = [re.sub("'", '', i) for i in habr_titles]
        habr_titles = [re.sub('"', '', i) for i in habr_titles]
    for title in range(0, len(habr_titles)):
        try:
            cursor.execute(
                """INSERT INTO news_app_post_habr (post_title, post_source, pub_date) VALUES ('{}', '{}', '{}')""".format(
                    habr_titles[title],
                    habr_links[title], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        except psycopg2.errors.UniqueViolation:
            pass
        except psycopg2.errors.InFailedSqlTransaction:
            pass


def get_habr():
    global habr_titles
    global habr_links
    global habr
    habr = 'https://habr.com/ru/news/'
    req = requests.get(habr).text
    soup = BeautifulSoup(req, 'lxml')
    posts = soup.find_all('a', class_='post__title_link')
    for link in posts:
        habr_links.append(link.get('href'))
        habr_titles.append(link.get_text())
    add_news('habr', habr_titles, habr_links)
    habr_titles = get_titles('habr')
    habr_links = get_links('habr')
    habr = []
    for i in range(0, len(habr_titles)):
        data = {
            'title': habr_titles[i],
            'link': habr_links[i],
        }

        habr.append(data)


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
    add_news('tproger', tproger_titles, tproger_links)
    tproger_titles = get_titles('tproger')
    tproger_links = get_links('tproger')


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
    for title in range(0, len(tproger_titles)):
        try:
            cursor.execute(
                """INSERT INTO news_app_post_tproger (post_title, post_source, pub_date) VALUES ('{}', '{}', '{}')""".format(
                    tproger_titles[title],
                    tproger_links[title], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        except psycopg2.errors.StringDataRightTruncation:
            pass
        except psycopg2.errors.UniqueViolation:
            pass
        except psycopg2.errors.InFailedSqlTransaction:
            pass


def get_dnews():
    global dnews_titles
    global dnews_links
    dnews = 'https://3dnews.ru/news/'
    req = requests.get(dnews).text
    soup = BeautifulSoup(req, 'lxml')
    posts = soup.find_all('a', class_='entry-header')
    for title in posts:
        dnews_titles.append(title.get_text('h1'))
        dnews_links.append(title.get('href'))
    dnews_links = ['https://3dnews.ru/' + dnew for dnew in dnews_links]
    add_news('dnews', dnews_titles, dnews_links)
    dnews_titles = get_titles('dnews')
    dnews_links = get_links('dnews')


def get_dnews1():
    global dnews_links
    global dnews_titles
    for i in reversed(range(1, 101)):
        dnews = 'https://3dnews.ru/news/page-{}.html'.format(i)
        req = requests.get(dnews).text
        soup = BeautifulSoup(req, 'lxml')
        posts = soup.find_all('a', class_='entry-header')
        for title in posts:
            dnews_titles.append(title.get_text('h1'))
            dnews_links.append(title.get('href'))
    dnews_links = ['https://3dnews.ru/' + dnew for dnew in dnews_links]
    dnews_titles = [re.sub("'", '', i) for i in dnews_titles]
    dnews_titles = [re.sub('"', '', i) for i in dnews_titles]
    for title in range(0, len(dnews_titles)):
        try:
            cursor.execute(
                """INSERT INTO news_app_post_dnews (post_title, post_source, pub_date) VALUES ('{}', '{}', '{}')""".format(
                    dnews_titles[title],
                    dnews_links[title], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        except psycopg2.errors.StringDataRightTruncation:
            pass
        except psycopg2.errors.UniqueViolation:
            pass
        except psycopg2.errors.InFailedSqlTransaction:
            pass


get_habr()


cursor.close()
connection.close()


def home(req):
    context = {
        'habr_titles': habr_titles,
        'habr_links': habr_links,
        'habr': habr
    }
    return render(req, 'news_app/home.html', context)
