# -*- encoding: gbk -*-

import requests
import json

url = 'https://public.creditchina.gov.cn/private-api/typeSourceSearch?source=&type=行政管理&searchState=1&entityType=1&scenes=defaultscenario&keyword=江苏华祝建设工程有限公司&tyshxydm=91320105780688132K&page=1&pageSize=10'

# 'https://www.creditchina.gov.cn/xinyongxinxixiangqing/xyDetail.html?searchState=1&entityType=1&keyword=' \
# '江苏华祝建设工程有限公司&uuid=7d5e8c35a8a6b3c42ff1b5029dcb13d6&tyshxydm=91320105780688132K'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/72.0.3626.109 Safari/537.36',
}
# response = requests.get(url=url, headers=headers)
# print(response.status_code)
# 使用session模拟
session = requests.session()
response = session.get(url=url, headers=headers).text
jl = json.loads(response)

mc = ['xk_wsh',
      'xk_xkws',
      'xk_xkzs',
      'xk_xklb',
      'xk_xkbh',
      'xk_jdrq',
      'xk_yxqz',
      'xk_yxqzi',
      'xk_nr',
      'xk_xkjg',
      'xk_xkjgdm',
      'xk_lydw',
      'xk_lydwdm']
qz_0 = jl['data']['list'][0]['entity'][mc[0]]
qz_1 = jl['data']['list'][0]['entity'][mc[1]]
qz_2 = jl['data']['list'][0]['entity'][mc[2]]
qz_3 = jl['data']['list'][0]['entity'][mc[3]]
qz_4 = jl['data']['list'][0]['entity'][mc[4]]
qz_5 = jl['data']['list'][0]['entity'][mc[5]]
qz_6 = jl['data']['list'][0]['entity'][mc[6]]
qz_7 = jl['data']['list'][0]['entity'][mc[7]]
qz_8 = jl['data']['list'][0]['entity'][mc[8]]
qz_9 = jl['data']['list'][0]['entity'][mc[9]]
qz_10 = jl['data']['list'][0]['entity'][mc[10]]
qz_11 = jl['data']['list'][0]['entity'][mc[11]]
qz_12 = jl['data']['list'][0]['entity'][mc[12]]

print(qz_0, qz_1, qz_2, qz_3, qz_4, qz_5, qz_6, qz_7, qz_8, qz_9, qz_10, qz_11, qz_12)
