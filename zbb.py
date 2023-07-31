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

dc = df.con_name
dp = df.con_p
de = df.con_am

con_name = input("请输入企业名称：")
for i in range(0, len(df)):
    m = dc[i]
    p = dp[i]
    n = de[i]
    if con_name == m:
        continue
print('企业的名称为:' + str(m))
print('企业人员数为:' + str(p))
print('企业资产数为:' + str(n))


def abbdpdlj():
    if p >= 5:
        a = '大傻逼'
        return a
    else:
        a1 = '小傻逼'
        return a1


print(abbdpdlj())
