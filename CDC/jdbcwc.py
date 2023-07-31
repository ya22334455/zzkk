# -*- coding: gbk -*-
import mysql.connector
import pandas as pd
import numpy as np

# 数据库配置
mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root"  # 数据库密码
)

cur = mydb.cursor()

sqlcom = 'select * from gql.runoob_tbl'

df = pd.read_sql(sqlcom, con=mydb)

ds = df.iloc[:, 1]

con_name = input("请输入企业名称：")

if con_name in ds.values:
    print("企业名称为：" + con_name)
    print("企业人员数为：" + str(df[df.con_name == con_name].con_p.values[0]))
    print("企业资产数为：" + str(df[df.con_name == con_name].con_am.values[0]))
    if df[df.con_name == con_name].con_p.values[0] >= 5:
        a = 10
    else:
        a = 5
    if df[df.con_name == con_name].con_am.values[0] >= 5:
        b = 10
    else:
        b = 5
    print("企业评分为：" + str(a + b))

