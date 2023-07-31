# -*- coding: utf-8 -*-
# Author:   miracle
# Date:     2022/4/11 21:51
import datetime
import json
import logging
import re
import time
import math

import pandas
import requests
from multiprocessing.dummy import Pool as ThreadPool

from lxml import etree

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


class hebeieb(object):

    def __init__(self):
        self.page = None
        self.num = None
        self.list_url = 'http://www.hebeieb.com/tender/xxgk/list.do?selectype=zbgg'  # 城市列表url
        self.proxy = dict()
        self.list_list = list()
        logging.basicConfig(level=logging.INFO,
                            format='%(message)s',
                            encoding='utf-8-sig',
                            filename='{}.csv'.format(__file__.split('/')[-1].split('.')[0]),
                            filemode='a')

        self._headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'JSESSIONID=230A13FDA874CB3E53DA7A5DE3A5C1F3; SF_cookie_1=35937142; __51cke__=; '
                      '__tins__19687679=%7B%22sid%22%3A%201687336755672%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A'
                      '%201687339494013%7D; __51laig__=5',
            'Host': 'www.hebeieb.com',
            'Origin': 'http://www.hebeieb.com',
            'Referer': 'http://www.hebeieb.com/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def get_response(self, url, params=None, method='get'):
        # 发送请求
        try:
            if method == 'get':
                res = requests.get(url, params=params, headers=self._headers, proxies=self.proxy, timeout=5)
                print(res)
            else:
                res = requests.post(url, data=params, headers=self._headers, proxies=self.proxy, timeout=5)
            if res.status_code == 200:
                return res
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_list(self, page):
        url = 'http://www.hebeieb.com/tender/xxgk/list.do?selectype=zbgg'
        params = {'page': page, 'TimeStr': '', 'allDq': '', 'allHy': 'reset1,', 'AllPtName': '', 'KeyStr': '',
                  'KeyType': 'ggname'}
        res = self.get_response(url, params=params, method='post')
        if res:
            data = etree.HTML(res.text)

            xiangmu = data.xpath('//*[@class="publicont"]//h4/a/text()')
            diqu = data.xpath('//*[@class="publicont"]//p/span[2]/text()')
            release_time = data.xpath('//*[@class="publicont"]//h4/span/text()')
            pingtai = data.xpath('//*[@class="publicont"]//p/span[4]/text()')
            href_list = data.xpath('//*[@class="publicont"]//a/@href')
            detail_params = {
                "xiangmu": self.handler(xiangmu),
                "diqu": self.handler(diqu),
                "release_time": self.handler(release_time),
                "pingtai": self.handler(pingtai),
                "href_list": self.handler(href_list)
            }

            self.get_detail_list(detail_params)
            print('---------第{}页抓取完成------------'.format(page))

    def get_detail_list(self, detail_params):
        url_list = detail_params['href_list']
        pingtai_list = detail_params['pingtai']
        xiangmu = detail_params['xiangmu']
        diqu = detail_params['diqu']
        release_time = detail_params['release_time']
        for i in range(len(url_list)):
            infoid = ''.join(re.findall(r'infoid=(.*?)&', url_list[i]))
            pingtai = pingtai_list[i]
            if '平台内' in pingtai:
                url = '/infogk/newDetail.do?categoryid=101103&infoid={}&laiyuan={}'.format(infoid, pingtai)
                res = self.get_response(self.list_url + url, method='post')

                data = self.handler(res.text)
                houxuan = re.findall('(中标候选人名单.*?</table>|中标候选人单位名称.*?</table>)', data, re.S)
                houxuan = re.findall('[\w\(\)（）]{5,}公司', ''.join(houxuan))
                houxuan = ','.join(houxuan)

                daili = re.findall('招标代理机构.*?([\w\(\)（）]{5,}公司)', data, re.S)
                if daili:
                    daili = daili[0]

                dailiPhone = re.findall('招标代理机构.*?电话.*电话.*?([\d/-]{10,})', data, re.S)
                if len(dailiPhone) >= 1:
                    dailiPhone = dailiPhone[-1]
                else:
                    dailiPhone = re.findall('招标代理机构.*?电话.*?([\d/-]{10,})', data, re.S)
                    if len(dailiPhone) >= 1:
                        dailiPhone = dailiPhone[-1]

                print('{},{},{},{},{},{}'.format(xiangmu[i], diqu[i], release_time[i], ''.join(daili),
                                                 ''.join(dailiPhone), houxuan))
                logging.info('{},{},{},{},{},{}'.format(xiangmu[i], diqu[i], release_time[i], ''.join(daili),
                                                        ''.join(dailiPhone), houxuan))

            else:
                url = '/infogk/newDetail.do?categoryid=101101&infoid={}&jypt=jypt'.format(infoid)
                res = self.get_response(self.list_url + url)

                data = self.handler(res.text)
                data = re.sub('打印.*$', '', data, re.S)

                houxuan = re.findall('(中标候选人名单.*?</table>|中标候选人单位名称.*?</table>)', data, re.S)
                if houxuan:
                    houxuan = re.findall('[\w\(\)（）]{5,}公司', ''.join(houxuan))
                    if len(houxuan) > 3:
                        houxuan = ','.join(houxuan[0:3])
                else:
                    houxuan = re.findall('第.中标候选人.*?([\w\(\)（）]{5,}公司)', data)
                if len(houxuan) > 3:
                    houxuan = houxuan[0:3]
                houxuan = ','.join(houxuan)

                daili = re.findall('招标代理机构.*?([\w\(\)（）]{5,}公司)', data, re.S)
                if daili:
                    daili = daili[0]

                dailiPhone = re.findall('招标代理机构.*?电.?话.*电.?话.*?([\d/-]{10,})', data, re.S)
                if len(dailiPhone) >= 1:
                    dailiPhone = dailiPhone[-1]
                else:
                    dailiPhone = re.findall('招标代理机构.*?电.?话.*?([\d/-]{10,})', data, re.S)
                    if len(dailiPhone) >= 1:
                        dailiPhone = dailiPhone[-1]

                print('{},{},{},{},{},{}'.format(xiangmu[i], diqu[i], release_time[i], ''.join(daili),
                                                 ''.join(dailiPhone), houxuan))
                logging.info('{},{},{},{},{},{}'.format(xiangmu[i], diqu[i], release_time[i], ''.join(daili),
                                                        ''.join(dailiPhone), houxuan))

    @staticmethod
    def handler(words):
        if isinstance(words, list):
            words = [x.replace('\n', '').replace('\r', '').replace('\t', '').replace('|', '').strip().replace(",", "，")
                     for x in words]
            return [i for i in words if i != '']
        elif isinstance(words, str):
            return words.replace('\n', '').replace('\r', '').replace('\t', '').replace('|', '').strip().replace(",",
                                                                                                                "，")

    @staticmethod
    def get_word(data_list, data, flag=None):
        word = ''
        for i in range(len(data_list)):
            if data in data_list[i]:
                if flag == 'self':
                    word = data_list[i]
                    data_list.pop(i)
                else:
                    word = data_list[i + 1]
                    data_list.pop(i)
                    data_list.pop(i)
                break
        return word, data_list

    def run_function(self, num, page):
        if num == '1':
            print(range(int(page[0]) - 1, int(page[1])))

            for i in range(int(page[0]) - 1, int(page[1])):
                self.get_list(i)
        else:

            url = 'http://www.hebeieb.com/tender/xxgk/list.do?selectype=zbgg'
            params = {'page': '', 'TimeStr': '', 'join(page)': '', 'allDq': '', 'allHy': 'reset1,', 'AllPtName': '',
                      'KeyStr': '', 'KeyType': 'name'}
            res = self.get_response(url, params=params, method='post')
            if res:
                page_count = ''.join(re.findall('共：(\d+)条', res.text))
                print(range(math.ceil(int(page_count) / 15)))

                for i in range(math.ceil(int(page_count) / 15) + 1):
                    self.get_list(i)
            else:
                print(111111111111)

    def run(self):
        num = input('请输入功能编号：\n1.获取列表\n2.获取详情\n')
        if num == '1':
            self.run_function(num, input('请输入页码，以逗号隔开\n').split(','))
        elif num == '2':
            self.run_function(num, input('请输入infoid，以逗号隔开\n').split(','))
        else:
            print('功能编号输入错误')


if __name__ == '__main__':
    t = hebeieb()
    t.run()
