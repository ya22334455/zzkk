# -*- coding: gbk -*-

# ����������ʷ����Ԥ�����˫ɫ����
redlist = [[1, 10, 12, 16, 17, 30], [9, 13, 14, 17, 19, 27], [11, 18, 23, 24, 31, 33]]
bluelist = [12, 3, 13]


# ���ɺ���Ԥ����
redresult = []
for i in range(6):
    redresult.append(redlist[0][i] + redlist[1][i] + redlist[2][i])
print("����Ԥ������", redresult)

# ��������Ԥ����
blueresult = bluelist[0] + bluelist[1] + bluelist[2]
print("����Ԥ������", blueresult)

