# -*- encoding: gbk -*-
import requests
import urllib
from urllib import parse

# 所需下载的公司名称
list_com = ['鲁能集团有限公司', '苏州鲁能置业有限公司', '郑州鲁能置业有限公司', '鲁京建设工程有限公司',
            '江苏华祝建设工程有限公司']
# 下载文件的保存路径
file_path = str('C:\\Users\\18339\\Desktop\\信用中国网站文件下载\\')
# 在此案例中使用requests访问URL必须加入headers以伪装成正常访问，否则会被信用中国网站屏蔽
# headers的获取方式自行百度即可
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
# URL的相同部分，用于拼成完整的URL
url1 = 'https://public.creditchina.gov.cn/credit-check/pdf/download?companyName='
url2 = '&entityType=1&uuid=&tyshxydm='

# 方便为文件编号
i = 1
for name in list_com:
    # 将公司名称转换为能被服务器读取的编码
    encode_name = urllib.parse.quote(name)
    # 拼成完整的URL
    url = url1 + encode_name + url2
    # 伪装成正常访问，完成文件下载
    r = requests.get(url, headers=headers)
    with open(file_path + str(i) + '-' + name + '.pdf', "wb") as code:
        code.write(r.content)
    # 随时反馈下载情况
    print('{}-{}'.format(i, name))
    i += 1
    