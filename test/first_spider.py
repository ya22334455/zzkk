#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re
import time
from faker import Factory
import requests
from lxml import etree
import json

url = 'http://kjj.hefei.gov.cn/public/column/2971?sub=&catId=6718761&nav=3&action=list&type=4&pageIndex=1'


def B(js2py=None, execjs=None):
    headers = {
        'Cookie': '__jsluid_h=2d08a6173999641305627ef610af78ad; '
                  '__jsl_clearance=1629450531.317|0|T68aGoBUCe0AodUL59%2BiqR%2BmItM%3D;',
        "Host": "kjj.hefei.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.131 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=3)
    js1 = re.findall('<script>(.+?)</script>', response.content.decode())[0].replace('document.cookie=', '').replace(
        'location.href=location.pathname+location.search', '')
    context = js2py.EvalJs()
    context.execute('cookies2 =' + js1)
    cookies = context.cookies2.split(';')[0].split('=')
    headers['Cookie'] = '__jsluid_h=2d08a6173999641305627ef610af78ad; {}={};'.format(cookies[0], cookies[1])
    cookie_js = requests.get(url, headers=headers).text
    cookie_param = json.loads(re.search(r'go\(({.+?})\)</script>', cookie_js).group(1))
    with open(r'js.js', 'r', encoding='utf-8') as f:
        js = f.read()
    while True:
        ct = execjs.compile(js, cwd=r'C:\Users\Datong\AppData\Roaming\npm\node_modules')
        cookie = ct.call('go', cookie_param).split(';')[0] + ';'
        if '__jsl_clearance=' in cookie:
            break
        time.sleep(1)
        B()
    headers['Cookie'] = '__jsluid_h=2d08a6173999641305627ef610af78ad; {}'.format(cookie)
    response = requests.get(url, headers=headers, timeout=3).text
    response = etree.HTML(response).xpath('//ul[@class="clearfix xxgk_nav_list"]/li')
    for x in response:
        print(x.xpath('.//a/@title')[0])


if __name__ == '__main__':
    B()
