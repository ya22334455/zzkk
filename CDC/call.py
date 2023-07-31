# -*- coding: gbk -*-
import mysql.connector


class AD:
    # 连接到MySQL数据库
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='gql'
    )
    # 创建游标
    cursor = conn.cursor()
    # 准备参数
    parameter = input("请输入一个企业名称：")
    # 执行存储过程
    cursor.callproc('AD', [parameter])
    # 获取存储过程的结果
    results = []
    for result in cursor.stored_results():
        results.append(result.fetchall())
    # 提交事务
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    # 打印结果转换为单个列表
    for result in results:
        print(result[0][0])
        # print(result)
