import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    table_news = parser.table.findAll('table')
    tr_tags = table_news[1].findAll('tr')
    for i in range(0, len(tr_tags)-2, 3):
        td_tags_first = tr_tags[i].findAll('td')
        #print('Новость: ')
        #print(td_tags_first[2].a.text) #название

        span_in_td_tags_first = td_tags_first[2].findAll('span')
        #    print(span_in_td_tags_first[1].text) #сайт

        td_tags_second = tr_tags[i + 1].findAll('td')
        span_in_td_tags_second = td_tags_second[1].findAll('span')
        points = 0
        if str(span_in_td_tags_second[0].text).find('points') >= 0:
            points = int(str(span_in_td_tags_second[0].text).split(' ')[0])

        #print(points) #лайки

        a_in_td_tags_second = td_tags_second[1].findAll('a')
        author = ''
        if str(a_in_td_tags_second[0]['href']).find('user') >= 0:
            author = a_in_td_tags_second[0].text


        #print(a_in_td_tags_second[0]['href'])
        #print(a_in_td_tags_second[0].text) #автор

        commentCount = 0
        if a_in_td_tags_second[len(a_in_td_tags_second) - 1].text != "discuss" and str(a_in_td_tags_second[len(a_in_td_tags_second) - 1].text).find('comment') >= 0:
            commentCount = int("".join((x for x in a_in_td_tags_second[len(a_in_td_tags_second) - 1].text if x.isdigit())))
        #print(commentCount) #комменты

        url = ''
        if len(span_in_td_tags_first) == 2:
            url = 'https://' + span_in_td_tags_first[1].text + '/'

        news = {'author': author,
                'comments': commentCount,
                'points' : points,
                'title': td_tags_first[2].a.text,
                 'url' : url}
        news_list.append(news)
    return news_list

def extract_next_page(parser):
    """ Extract next page URL """

    table_news = parser.table.findAll('table')
    tr_tags = table_news[1].findAll('tr')
    return tr_tags[len(tr_tags) - 1].findAll('a')[0]['href']

def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news