# -*- coding: gbk -*-
import mysql.connector


class AD:
    # ���ӵ�MySQL���ݿ�
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='gql'
    )
    # �����α�
    cursor = conn.cursor()
    # ׼������
    parameter = input("������һ����ҵ���ƣ�")
    # ִ�д洢����
    cursor.callproc('AD', [parameter])
    # ��ȡ�洢���̵Ľ��
    results = []
    for result in cursor.stored_results():
        results.append(result.fetchall())
    # �ύ����
    conn.commit()
    # �ر�����
    cursor.close()
    conn.close()
    # ��ӡ���ת��Ϊ�����б�
    for result in results:
        print(result[0][0])
        # print(result)
