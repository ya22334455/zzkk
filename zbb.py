# -*- coding: gbk -*-
import mysql.connector
import pandas as pd
import numpy as np

# ���ݿ�����
mydb = mysql.connector.connect(
    host="localhost",  # ���ݿ�������ַ
    user="root",  # ���ݿ��û���
    passwd="root"  # ���ݿ�����
)

cur = mydb.cursor()

sqlcom = 'select * from gql.runoob_tbl'

df = pd.read_sql(sqlcom, con=mydb)

dc = df.con_name
dp = df.con_p
de = df.con_am

con_name = input("��������ҵ���ƣ�")
for i in range(0, len(df)):
    m = dc[i]
    p = dp[i]
    n = de[i]
    if con_name == m:
        continue
print('��ҵ������Ϊ:' + str(m))
print('��ҵ��Ա��Ϊ:' + str(p))
print('��ҵ�ʲ���Ϊ:' + str(n))


def abbdpdlj():
    if p >= 5:
        a = '��ɵ��'
        return a
    else:
        a1 = 'Сɵ��'
        return a1


print(abbdpdlj())
