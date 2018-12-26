# -*- coding: utf-8 -*-
from spider import Spider
import requests
from bs4 import BeautifulSoup


class DouBan(Spider):

    def __init__(self):
        super(DouBan, self).__init__()
        self.start_url = 'https://movie.douban.com/top250'
        self.filename = 'douban.json' # 覆盖默认值
        self.output_result = False
        self.thread_num = 10

    def start_requests(self): # 覆盖默认函数
        yield (self.start_url, self.parse_first)

    def parse_first(self, url): # 只需要yield待爬url和回调函数
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        movies = soup.find_all('div', class_ = 'info')[:5]
        for movie in movies:
            url = movie.find('div', class_ = 'hd').a['href']
            yield (url, self.parse_second)

        next_page = soup.find('span', class_ = 'next').a
        if next_page:
            next_url = self.start_url + next_page['href']
            yield (next_url, self.parse_first)
        else:
            self.running = False # 表明运行到这里则不会继续添加待爬URL队列

    def parse_second(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        my_dict = {}
        title = soup.find('span', property = 'v:itemreviewed')
        my_dict['title'] = title.text if title else None
        duration = soup.find('span', property = 'v:runtime')
        my_dict['duration'] = duration.text if duration else None
        time = soup.find('span', property = 'v:initialReleaseDate')
        my_dict['time'] = time.text if time else None
        yield my_dict


if __name__ == '__main__':
    douban = DouBan()
    douban.run()