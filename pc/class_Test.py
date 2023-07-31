# -*- encoding: gbk -*-
import requests
import random
from io import StringIO
from PIL import Image
import json
import urllib3

headers = {
    "Cookie": "JSESSIONID=A0053804D456749B5C08F489E3F1D9C2; _gscu_15322769=63264781iz6igj44; _gscbrs_15322769=1; "
              "Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1563264782; "
              "Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1563264782; _gscs_15322769=63264781zftbxy44|pv:3",
    "Host": "zxgk.court.gov.cn",
    "Origin": "http://zxgk.court.gov.cn",
    "Referer": "http://zxgk.court.gov.cn/shixin/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Mobile Safari/537.36"
}


def getNum():
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
             'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
             'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
             'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
             'x', 'y', 'z']
    nums = ""
    for i in range(0, 32):
        id = int(random.randint(0, 61))
        nums += chars[id]
    return nums


captchaId = getNum().replace("-", "")
print(captchaId)
randomNumber = str(random.random())
uuid = str(getNum())
imgs = "http://zxgk.court.gov.cn/shixin/captchaNew.do?captchaId=" + str(captchaId) + "&random=" + randomNumber
print(imgs)
rims = requests.get(url=imgs, headers=headers).content
with open("../a.png", "wb") as f:
    f.write(rims)
pcode = input("请输入验证码：")
data = {
    'pName': '四川创业融资担保有限公司',
    'pProvince': '0',
    'pCode': pcode,
    'captchaId': captchaId,
    'currentPage': '1'
}
response = requests.post(url='http://zxgk.court.gov.cn/shixin/searchSX.do', headers=headers, data=data)
print(response)
html = response.content.decode("utf-8")
html = json.loads(json.dumps(html))
print(html)
