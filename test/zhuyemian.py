#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import urllib3
import urllib
import time
import re

from selenium.webdriver.common.devtools.v85.page import reload

reload(sys)
sys.setdefaultencoding('utf8')

headers = ("User-Agent",
           "Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/60.0")
opener = urllib3.build_opener()
opener.addheaders = [headers]
urllib3.install_opener(opener)

for i in range(1, 1500):
    url = "http://shixin.court.gov.cn/captchaNew.do?captchaId=6eb54a8c64f84a84b6490db24671c310&random=" + str(i)
    data = urllib3.urlopen(url).read()
    # data=urllib2.quote(data).decode('utf-8')
    file = "/home/yang/png/test/" + str(i) + ".png"
    playFile = open(file, 'wb')
    playFile.write(data)
    playFile.close()
    time.sleep(1)