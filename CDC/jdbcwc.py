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

ds = df.iloc[:, 1]

con_name = input("��������ҵ���ƣ�")

if con_name in ds.values:
    print("��ҵ����Ϊ��" + con_name)
    print("��ҵ��Ա��Ϊ��" + str(df[df.con_name == con_name].con_p.values[0]))
    print("��ҵ�ʲ���Ϊ��" + str(df[df.con_name == con_name].con_am.values[0]))
    if df[df.con_name == con_name].con_p.values[0] >= 5:
        a = 10
    else:
        a = 5
    if df[df.con_name == con_name].con_am.values[0] >= 5:
        b = 10
    else:
        b = 5
    print("��ҵ����Ϊ��" + str(a + b))

