# -*- encoding: gbk -*-
import requests
import urllib
from urllib import parse

# �������صĹ�˾����
list_com = ['³�ܼ������޹�˾', '����³����ҵ���޹�˾', '֣��³����ҵ���޹�˾', '³�����蹤�����޹�˾',
            '���ջ�ף���蹤�����޹�˾']
# �����ļ��ı���·��
file_path = str('C:\\Users\\18339\\Desktop\\�����й���վ�ļ�����\\')
# �ڴ˰�����ʹ��requests����URL�������headers��αװ���������ʣ�����ᱻ�����й���վ����
# headers�Ļ�ȡ��ʽ���аٶȼ���
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
# URL����ͬ���֣�����ƴ��������URL
url1 = 'https://public.creditchina.gov.cn/credit-check/pdf/download?companyName='
url2 = '&entityType=1&uuid=&tyshxydm='

# ����Ϊ�ļ����
i = 1
for name in list_com:
    # ����˾����ת��Ϊ�ܱ���������ȡ�ı���
    encode_name = urllib.parse.quote(name)
    # ƴ��������URL
    url = url1 + encode_name + url2
    # αװ���������ʣ�����ļ�����
    r = requests.get(url, headers=headers)
    with open(file_path + str(i) + '-' + name + '.pdf', "wb") as code:
        code.write(r.content)
    # ��ʱ�����������
    print('{}-{}'.format(i, name))
    i += 1
    