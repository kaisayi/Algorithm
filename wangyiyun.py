#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-13 20:13:09
# Project: wangyi_music

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) ' \
                 'Gecko/20100101 Firefox/55.0'

    crawl_config = {
        'headers': {
            'User-Agent': user_agent
        },
        'allow_redirects': False

    }

    retry_delay = {
        0: 50 * 60,
        '': 30 * 60,
    }

    def get_headers(self):
        return {
            'Host': 'music.163.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://music.163.com/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cookie': '_ntes_nnid=49eac0ac666043bd4ab00575d32f97cd,1503045349716; '
                      '_ntes_nuid=49eac0ac666043bd4ab00575d32f97cd; '
                      '__csrf=01ffd84cd2958b9caa1ad145a45ee798; '
                      'JSESSIONID-WYYY=jCHI7VTPIS07ryMeaQcpZxzUAaZ6XYA%2FAOxiTW4NDiu5nrhYx0RDVR1%2FGw%2FQcc5OtcKJHmWPC%2B2OY6OXi5qEAzM0jg8HWvboK3gpxtlNnSv3J2pXsOUeK75fHXSUFERa9Cfr9Siio1JWYSSGzCpUcOusmxQuXJ0mbrUUF6cmUkfvvoO8%3A1503914349464; '
                      '_iuqxldmzr_=32; '
                      '__utma=94650624.1618839228.1503045350.1503886642.1503912550.3; '
                      '__utmb=94650624.9.10.1503912550; __utmc=94650624; '
                      '__utmz=94650624.1503912550.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
        }


    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://music.163.com/discover/playlist/',
                   method='GET',
                   headers=self.get_headers(),
                   callback=self.list_page)

    def list_page(self, response):
        d = response.doc
        for each in d('a.s-fc1').items():
            self.crawl(each.attr.href, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        url = response.url
        limit = 35
        d1 = response.doc
        total_page_num = int(d1('a.zpgi:last').text())
        for num in range(total_page_num):
            self.crawl(url,
                       params={'order': 'hot',
                               'limit': str(limit),
                               'offset': str(num*limit)},
                       callback=self.next_page)

    def next_page(self, response):
        d2 = response.doc
        for each in d2('.dec > a'):
            self.crawl(each.attr.href,
                       callback=self.music_page)

    def music_page(self, response):
        d3 = response.doc
        for each in d3('ul.f_hide a').items():
            self.crawl(each.attr.href,
                       callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        doc = response.doc
        return {
            'url': response.url,
            'song_name': doc('em.f-ff2').text(),

        }
