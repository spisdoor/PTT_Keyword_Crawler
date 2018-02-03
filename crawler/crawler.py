import urllib
from bs4 import BeautifulSoup
import requests

def getPrePageUrl(soup):
    for btn in soup.select('.wide'):
        if btn.text == '‹ 上頁':
            return btn['href']

def getByArticleTitle(name, page_num, keyword):
    PTT_URL = 'https://www.ptt.cc'
    cur_page_url = 'https://www.ptt.cc/bbs/' + name + '/index.html'
    article_title = []
    payload = {
        'from' : '/bbs/' + name + '/index.html',
        'yes' : 'yes'
    }
    rs = requests.session()
    for i in range(page_num):
        res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
        res = rs.get(cur_page_url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')

        titles = soup.select('.title')
        for title in titles:
            if keyword in title.text.strip('\n'):
                article_title.append([title.text.strip('\n'), PTT_URL + title.find('a')['href']])
        cur_page_url = PTT_URL + getPrePageUrl(soup)
    return article_title

def getByArticleContent(name, page_num, keyword):
    PTT_URL = 'https://www.ptt.cc'
    cur_page_url = 'https://www.ptt.cc/bbs/' + name + '/index.html'
    article_content = []
    payload = {
        'from' : '/bbs/' + name + '/index.html',
        'yes' : 'yes'
    }
    rs = requests.session()
    for i in range(page_num):
        # 瀏覽文章標題頁
        res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
        res = rs.get(cur_page_url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('.title')
        cur_page_url = PTT_URL + getPrePageUrl(soup)
        for title in titles:
            # 每篇文章頁
            if not title.find('a'):
                # 該篇文章被刪除
                continue
            url = title.find('a')['href']
            per_article = requests.get(PTT_URL + url)
            soup = BeautifulSoup(per_article.text, 'html.parser')

            content = soup.select('#main-content')
            for div in content[0].find_all("div", {'class':['article-metaline','article-metaline-right','push','richcontent']}): 
                div.decompose()
            if keyword in content[0].text:
                article_content.append([content[0].text, title.text, PTT_URL + url])
    return article_content

def getByArticleMessage(name, page_num, keyword):
    PTT_URL = 'https://www.ptt.cc'
    cur_page_url = 'https://www.ptt.cc/bbs/' + name + '/index.html'
    article_message = []
    payload = {
        'from' : '/bbs/' + name + '/index.html',
        'yes' : 'yes'
    }
    rs = requests.session()
    for i in range(page_num):
        # 瀏覽文章標題頁
        res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
        res = rs.get(cur_page_url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('.title')
        cur_page_url = PTT_URL + getPrePageUrl(soup)
        for title in titles:
            # 每篇文章頁
            if not title.find('a'):
                # 該篇文章被刪除
                continue
            url = title.find('a')['href']
            per_article = requests.get(PTT_URL + url)
            soup = BeautifulSoup(per_article.text, 'html.parser')

            msg = soup.select('.push')
            for i in range(len(msg)):
                if keyword in msg[i].select('.push-content')[0].text.strip('\n'):
                    for span in msg[i].find_all("span", {'class':['push-ipdatetime']}): 
                        span.decompose()
                    ###############
                    j = i - 1
                    temp = []
                    while j:
                        if msg[j].select('.push-userid') == msg[i].select('.push-userid'):
                            for span in msg[j].find_all("span", {'class':['push-ipdatetime']}): 
                                span.decompose()
                            temp.insert(0, [msg[j].text.strip('\n'), title.text, PTT_URL + url])
                        else:
                            break;
                        j = j - 1
                    for t in temp:
                        article_message.append(t)
                    ###############
                    article_message.append([msg[i].text.strip('\n'), title.text, PTT_URL + url])
                    ###############
                    j = i + 1
                    temp = []
                    while j and j < len(msg):
                        if (msg[j].select('.push-userid') == msg[i].select('.push-userid')) and (keyword not in msg[j].select('.push-content')[0].text.strip('\n')):
                            for span in msg[j].find_all("span", {'class':['push-ipdatetime']}): 
                                span.decompose()
                            temp.insert(0, [msg[j].text.strip('\n'), title.text, PTT_URL + url])
                        else:
                            break;
                        j = j + 1
                    for t in temp:
                        article_message.append(t)
                    ###############
    return article_message
