# -*- encoding: gbk -*-
import requests
import json

a = []


def iskong(a):
    if len(str(a)) == 0:
        return ''
    else:
        return str(a)


name = input("��������ȡ����ַ:")
url = 'https://www.creditchina.gov.cn/api/credit_info_search?&templateId=&page=1&pageSize=10'
'https://www.creditchina.gov.cn/xinyongxinxixiangqing/xyDetail.html?searchState=1&entityType=1&keyword=' \
'���ջ�ף���蹤�����޹�˾&uuid=7d5e8c35a8a6b3c42ff1b5029dcb13d6&tyshxydm=91320105780688132K'

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

    print("��ʼ��ȡ-----{}------����ҳ".format(gongsi['name']))

    base_url = 'https://www.creditchina.gov.cn/api/credit_info_detail?encryStr=' + gongsi['encryStr'].replace('\n', '')

    response1 = requests.get(base_url, headers=headers)

    info_list = json.loads(response1.content.decode('utf-8'))
    if info_list:
        print("���ڲ�ѯ��ϸ��Ϣ�����Ժ�----")
        if len(info_list['result']) == 0:
            with open(info_list['entName'] + 'txt', 'a') as fp:
                fp.write("�޽��")
        else:
            info_list1 = info_list['result']
            print('-----��ҳ��Ϣ-----')
            print('��˾���ƣ�', iskong(info_list1['entName']))
            print('ͳһ�����Ϣ���룺', iskong(info_list1['creditCode']))
            print('��˾��ַ��', iskong(info_list1['dom']))
            print('�鿴����ʱ�䣺', iskong(info_list['timestatmp']))
            print("����ץȡ������Ϣ------")
            print('----������Ϣ----')
            print('����ע���', iskong(info_list1['regno']))
            print('���˴���', iskong(info_list1['legalPerson']))
            print('����ʱ��', iskong(info_list1['esdate']))
            print('��ҵ����', iskong(info_list1['enttype']))
            print('�Ǽǻ���', iskong(info_list1['regorg']))
            a = ('��˾���ƣ�' + iskong(info_list1['entName']) +
                 '\n' + 'ͳһ�����Ϣ���룺' + iskong(info_list1['creditCode'])
                 + '\n' + '��˾��ַ��' + iskong(info_list1['dom']) + '\n' +
                 '�鿴����ʱ�䣺' + iskong(info_list['timestatmp']) + '\n'
                 + '����ע��ţ�' + iskong(info_list1['regno']) + '\n' +
                 '���˴���' + iskong(info_list1['legalPerson']) + '\n' +
                 '����ʱ�䣺' + iskong(info_list1['esdate']) + '\n' +
                 '��ҵ���ͣ�' + iskong(info_list1['enttype']) + '\n' +
                 '�Ǽǻ��أ�' + iskong(info_list1['regorg']))
            a = a.replace('��', "��\n")
            print(a)
            with open(info_list1['entName'] + 'txt', 'w') as fp:
                fp.write(str(a))

    print('��ʼ��ȡ�����������----')
    print('----�����������--------')
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
                    fp.write("�޽��")
            else:
                i = info_list['result']['results'][0]

                print("������ɾ������ĺţ�", iskong(str(i['xkWsh'])))
                print("������ͣ�", iskong(i['xkSplb']))
                print("���˴�����������", iskong(i['xkFr']))
                print("������ɣ�", iskong(i['xkNr']))
                print("�����Ч�ڣ�", iskong(i['xkYxq']))
                print("��ɾ������ڣ�", iskong(i['xkJdrq']))
                print("�����Ч���ڣ�", iskong(i['xkJzq']))
                print("�ط����룺", iskong(i['xkDfbm']))
                print("���ݸ������ڣ�", iskong(i['xkSjc']))
                b = "������ɾ������ĺţ�" + \
                    '\n' + iskong(str(i['xkWsh'])) + \
                    '\n' + "������ͣ�" + '\n' + \
                    iskong(i['xkSplb']) + '\n' + \
                    "���˴�����������" + '\n' + \
                    iskong(i['xkFr']) + \
                    '\n' + "������ɣ�" + \
                    '\n' + iskong(i['xkNr']) + '\n' + \
                    "�����Ч�ڣ�" + iskong(i['xkYxq']) + \
                    '\n' + "��ɾ������ڣ�" + iskong(i['xkJdrq']) + \
                    '\n' + "�����Ч���ڣ�" + iskong(i['xkJzq']) + \
                    '\n' + "�ط����룺" + iskong(i['xkDfbm']) + \
                    '\n' + "���ݸ������ڣ�" + iskong(i['xkSjc'])

                with open(info_list1['entName'] + 'txt', 'a') as fp:
                    fp.write(str(b))
    except:
        pass

    print("������ȡ���ź����������Ժ�-------")

    try:
        url = 'https://www.creditchina.gov.cn/api/record_param?&creditType=2&dataSource=0&pageNum=1&pageSize=10&encryStr=' + \
              gongsi['encryStr'].replace('\n', '')
        response = requests.get(url, headers=headers)
        if info_list:
            info_list = json.loads(response.content.decode('utf-8'))
            if len(info_list['result']) == 0:
                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write("�޽��")

            else:
                i = info_list['result'][0]
                print("�������", iskong(i['�������']))
                print("������Դ", iskong(i['������Դ']))
                print("���", iskong(i['���']))
                print("��˰������", iskong(i["��˰������"]))
                print("�������", iskong(i["�������"]))
                print("���¸�������", iskong(i["���¸�������"]))
                print("�ļ���", iskong(i['�ļ���']))
                c = "�������" + iskong(i['�������']) + '\n' + \
                    "������Դ" + iskong(i['������Դ']) + '\n' + \
                    "���" + iskong(i['���']) + '\n' + \
                    "��˰������" + iskong(i["��˰������"]) + '\n' + \
                    "�������" + iskong(i["�������"]) + '\n' + \
                    "���¸�������" + iskong(i["���¸�������"]) + '\n' + \
                    "�ļ���" + iskong(i['�ļ���'])

                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write(str(c))

    except:
        pass

    print("������ȡ�ص��ע����")
    print("��ȡ�У����Ժ�.....")
    try:
        url = 'https://www.creditchina.gov.cn/api/record_param?creditType=4&dataSource=0&pageNum=1&pageSize=10&encryStr=' + \
              gongsi['encryStr'].replace('\n', '')
        response = requests.get(url, headers=headers)
        info_list = json.loads(response.content.decode('utf-8'))
        if info_list:
            if len(info_list['result']) == 0:
                print("���ص��ע���")
                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write("���ص��ע���")
            else:
                i = info_list['result'][0]
                print('��ҵ����', iskong(i['��ҵ����']))
                print('���������������', iskong(i['���������������']))
                print('���뾭Ӫ�쳣��¼ԭ����������', iskong(i['���뾭Ӫ�쳣��¼ԭ����������']))
                print('������Դ', iskong(i['������Դ']))
                print('�������', iskong(i['�������']))
                print('���¸�������', iskong(i['���¸�������']))
                print('����������', iskong(i['����������']))
                print('ע���', iskong(i['ע���']))
                print('��������', iskong(i['��������']))
                c = '��ҵ����' + iskong(i['��ҵ����']) + '\n' + \
                    '���������������' + iskong(i['���������������']) + '\n' + \
                    '���뾭Ӫ�쳣��¼ԭ����������' + iskong(i['���뾭Ӫ�쳣��¼ԭ����������']) + '\n' + \
                    '������Դ' + iskong(i['������Դ']) + '\n' + \
                    '�������' + iskong(i['�������']) + '\n' + \
                    '���¸�������' + iskong(i['���¸�������']) + '\n' + \
                    '����������' + iskong(i['����������']) + '\n' + \
                    'ע���' + iskong(i['ע���']) + '\n'
                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write(str(c))

                with open(info_list['entName'] + 'txt', 'a') as fp:
                    fp.write(str(c))
    except:
        pass

    print("ȫ����ȡ���")












