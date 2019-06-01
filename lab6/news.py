# -*- coding: utf-8 -*-

from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


url = 'https://news.ycombinator.com/newest?n=1'

@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    s.close()
    return template('news_template',  rows=rows)

@route('/add_label/')
def add_label():
    s=session()
    label = request.query['label']
    id = request.query['id']
    row = s.query(News).filter(News.id==id).first() #записи из бд с соответствующим id
    row.label = label #изменяем значение метки на label
    s.commit()
    s.close()
    redirect('/news')


@route('/update')
def update_news():
    s = session()
    sol = get_news(url)

    for lst in sol:
        title = lst['title']
        author = lst['author']
        if s.query(News).filter(News.title == title and News.author == author).count() == 0:
            new = News(title=lst['title'], 
                author=lst['author'], 
                url=lst['url'],
                comments=lst['comments'], 
                points=lst['points']
                )
            s.add(new)
            s.commit()

    s.close()
    redirect('/news')

@route('/classify')
def classify():
    s = session()

    g_list = []
    n_list = []
    m_list = []

    for row in s.query(News).filter(News.label == 'good').all():
        for i in (row.title + row.author).split():
            g_list.append(i.upper())
    for row in s.query(News).filter(News.label == 'never').all():
        for i in (row.title + row.author).split():
            n_list.append(i.upper())
    for row in s.query(News).filter(News.label == 'maybe').all():
        for i in (row.title + row.author).split():
            m_list.append(i.upper())


    #Считаем вероятность новости с какой-либо пометкой среди всех новостей
    chance_g = len(s.query(News).filter(News.label == 'good').all()) / len(s.query(News).all())
    chance_n = len(s.query(News).filter(News.label == 'never').all()) / len(s.query(News).all())
    chance_m = len(s.query(News).filter(News.label == 'maybe').all()) / len(s.query(News).all())

    for row in s.query(News).filter(News.label == None).all(): #Работаем с неразмеченными новостями
        #mini_dict = {}
        word_list = []#[str(w) for w in (row.title + row.author).split()]

        for i in (row.title + row.author).split():
            word_list.append(i.upper())

        chance_good = 0
        chance_never = 0
        chance_maybe = 0

        for i in word_list:
            if i in g_list:
                chance_good += g_list.count(i) / len(g_list)
            if i in n_list:
                chance_never += n_list.count(i) / len(n_list)
            if i in m_list:
                chance_maybe += m_list.count(i) / len(m_list)
        good = chance_g + chance_good
        never = chance_n + chance_never
        maybe = chance_m + chance_maybe

        if good >= never and good >= maybe:
            row.label = 'good'
        elif maybe > good and maybe >= never:
            row.label = 'maybe'
        elif never > good and never > maybe:
            row.label = 'never'
        s.commit()
    s.close()


@route('/special_news')
def spec_news():
    s = session()
    if len(s.query(News).filter(News.label == None).all()) != 0:
        classify()
    rows = s.query(News).order_by(News.label).all()
    return template('news_template2', rows=rows)


def database(list):
    s = session()
    for i in list:
        row = News(title=i['title'],
                   author=i['author'],
                   url=i['url'],
                   comments=i['comments'],
                   points=i['points'])
        s.add(row)

    s.commit()
    s.close()

if __name__ == '__main__':
    # solution = get_news()
    # database(solution)
    # n = news_list()
    # f = classify()
    run(host='localhost', port=8080)
    # a = add_label()
    # b = update_news()