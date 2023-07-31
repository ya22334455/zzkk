# -*- encoding: gbk -*-
import requests
import json

a = []


def iskong(a):
    if len(str(a)) == 0:
        return ''
    else:
        return str(a)


name = input("请输入爬取的网址:")
url = 'https://www.creditchina.gov.cn/api/credit_info_search?&templateId=&page=1&pageSize=10'
'https://www.creditchina.gov.cn/xinyongxinxixiangqing/xyDetail.html?searchState=1&entityType=1&keyword=' \
'江苏华祝建设工程有限公司&uuid=7d5e8c35a8a6b3c42ff1b5029dcb13d6&tyshxydm=91320105780688132K'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/72.0.3626.109 Safari/537.36',
}
data = {
    'keyword': name
}
response = requests.get(url=url, headers=headers, params=data).text
info_list = json.loads(response)

for gongsi in info_list['data']['results']:
    print()

    print("开始爬取-----{}------详情页".format(gongsi['name']))

    base_url = 'https://www.creditchina.gov.cn/api/credit_info_detail?encryStr=' + gongsi['encryStr'].replace('\n', '')

    response1 = requests.get(base_url, headers=headers)

    info_list = json.loads(response1.content.decode('utf-8'))
    if info_list:
        print("正在查询详细信息，请稍后----")
        if len(info_list['result']) == 0:
            with open(info_list['entName'] + 'txt', 'a') as fp:
                fp.write("无结果")
        else:
            info_list1 = info_list['result']
            print('-----首页信息-----')
            print('公司名称：', iskong(info_list1['entName']))
            print('统一社会信息代码：', iskong(info_list1['creditCode']))
            print('公司地址：', iskong(info_list1['dom']))
            print('查看报告时间：', iskong(info_list['timestatmp']))
            print("正在抓取基本信息------")
            print('----基本信息----')
            print('工商注册号', iskong(info_list1['regno']))
            print('法人代表', iskong(info_list1['legalPerson']))
            print('成立时间', iskong(info_list1['esdate']))
            print('企业类型', iskong(info_list1['enttype']))
            print('登记机关', iskong(info_list1['regorg']))
            a = ('公司名称：' + iskong(info_list1['entName']) +
                 '\n' + '统一社会信息代码：' + iskong(info_list1['creditCode'])
                 + '\n' + '公司地址：' + iskong(info_list1['dom']) + '\n' +
                 '查看报告时间：' + iskong(info_list['timestatmp']) + '\n'
                 + '工商注册号：' + iskong(info_list1['regno']) + '\n' +
                 '法人代表：' + iskong(info_list1['legalPerson']) + '\n' +
                 '成立时间：' + iskong(info_list1['esdate']) + '\n' +
                 '企业类型：' + iskong(info_list1['enttype']) + '\n' +
                 '登记机关：' + iskong(info_list1['regorg']))
            a = a.replace('：', "：\n")
            print(a)
            with open(info_list1['entName'] + 'txt', 'w') as fp:
                fp.write(str(a))

    print('开始爬取行政许可文书----')
    print('----行政许可文书--------')
    try:
        info_list1 = info_list['result']
        data = {
            'name': iskong(info_list1['entName'])
        }
        url = 'https://www.creditchina.gov.cn/api/pub_permissions_name?&page=1&pageSize=10'
        response2 = requests.get(url, params=data, headers=headers)
        info_list = json.loads(response2.content.decode('utf-8'))
        if info_list:
            # print(info_list['result']['results'][0]['xkWsh'])
            if info_list['result']['results'] == 0:
                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write("无结果")
            else:
                i = info_list['result']['results'][0]

                print("行政许可决定书文号：", iskong(str(i['xkWsh'])))
                print("审核类型：", iskong(i['xkSplb']))
                print("法人代表人姓名：", iskong(i['xkFr']))
                print("内容许可：", iskong(i['xkNr']))
                print("许可有效期：", iskong(i['xkYxq']))
                print("许可决定日期：", iskong(i['xkJdrq']))
                print("许可有效日期：", iskong(i['xkJzq']))
                print("地方编码：", iskong(i['xkDfbm']))
                print("数据更新日期：", iskong(i['xkSjc']))
                b = "行政许可决定书文号：" + \
                    '\n' + iskong(str(i['xkWsh'])) + \
                    '\n' + "审核类型：" + '\n' + \
                    iskong(i['xkSplb']) + '\n' + \
                    "法人代表人姓名：" + '\n' + \
                    iskong(i['xkFr']) + \
                    '\n' + "内容许可：" + \
                    '\n' + iskong(i['xkNr']) + '\n' + \
                    "许可有效期：" + iskong(i['xkYxq']) + \
                    '\n' + "许可决定日期：" + iskong(i['xkJdrq']) + \
                    '\n' + "许可有效日期：" + iskong(i['xkJzq']) + \
                    '\n' + "地方编码：" + iskong(i['xkDfbm']) + \
                    '\n' + "数据更新日期：" + iskong(i['xkSjc'])

                with open(info_list1['entName'] + 'txt', 'a') as fp:
                    fp.write(str(b))
    except:
        pass

    print("正在爬取守信红名单，请稍后-------")

    try:
        url = 'https://www.creditchina.gov.cn/api/record_param?&creditType=2&dataSource=0&pageNum=1&pageSize=10&encryStr=' + \
              gongsi['encryStr'].replace('\n', '')
        response = requests.get(url, headers=headers)
        if info_list:
            info_list = json.loads(response.content.decode('utf-8'))
            if len(info_list['result']) == 0:
                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write("无结果")

            else:
                i = info_list['result'][0]
                print("数据类别", iskong(i['数据类别']))
                print("数据来源", iskong(i['数据来源']))
                print("序号", iskong(i['序号']))
                print("纳税人名称", iskong(i["纳税人名称"]))
                print("评价年度", iskong(i["评价年度"]))
                print("最新更新日期", iskong(i["最新更新日期"]))
                print("文件名", iskong(i['文件名']))
                c = "数据类别" + iskong(i['数据类别']) + '\n' + \
                    "数据来源" + iskong(i['数据来源']) + '\n' + \
                    "序号" + iskong(i['序号']) + '\n' + \
                    "纳税人名称" + iskong(i["纳税人名称"]) + '\n' + \
                    "评价年度" + iskong(i["评价年度"]) + '\n' + \
                    "最新更新日期" + iskong(i["最新更新日期"]) + '\n' + \
                    "文件名" + iskong(i['文件名'])

                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write(str(c))

    except:
        pass

    print("正在爬取重点关注名单")
    print("爬取中，请稍后.....")
    try:
        url = 'https://www.creditchina.gov.cn/api/record_param?creditType=4&dataSource=0&pageNum=1&pageSize=10&encryStr=' + \
              gongsi['encryStr'].replace('\n', '')
        response = requests.get(url, headers=headers)
        info_list = json.loads(response.content.decode('utf-8'))
        if info_list:
            if len(info_list['result']) == 0:
                print("无重点关注情况")
                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write("无重点关注情况")
            else:
                i = info_list['result'][0]
                print('企业名称', iskong(i['企业名称']))
                print('列入决定机关名称', iskong(i['列入决定机关名称']))
                print('列入经营异常名录原因类型名称', iskong(i['列入经营异常名录原因类型名称']))
                print('数据来源', iskong(i['数据来源']))
                print('数据类别', iskong(i['数据类别']))
                print('最新更新日期', iskong(i['最新更新日期']))
                print('法定代表人', iskong(i['法定代表人']))
                print('注册号', iskong(i['注册号']))
                print('设立日期', iskong(i['设立日期']))
                c = '企业名称' + iskong(i['企业名称']) + '\n' + \
                    '列入决定机关名称' + iskong(i['列入决定机关名称']) + '\n' + \
                    '列入经营异常名录原因类型名称' + iskong(i['列入经营异常名录原因类型名称']) + '\n' + \
                    '数据来源' + iskong(i['数据来源']) + '\n' + \
                    '数据类别' + iskong(i['数据类别']) + '\n' + \
                    '最新更新日期' + iskong(i['最新更新日期']) + '\n' + \
                    '法定代表人' + iskong(i['法定代表人']) + '\n' + \
                    '注册号' + iskong(i['注册号']) + '\n'
                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write(str(c))

                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write(str(c))
    except:
        pass

    print("全部爬取完毕")












