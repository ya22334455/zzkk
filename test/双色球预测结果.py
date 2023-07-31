# -*- coding: gbk -*-

# 根据三组历史数据预测今晚双色球结果
redlist = [[1, 10, 12, 16, 17, 30], [9, 13, 14, 17, 19, 27], [11, 18, 23, 24, 31, 33]]
bluelist = [12, 3, 13]


# 生成红球预测结果
redresult = []
for i in range(6):
    redresult.append(redlist[0][i] + redlist[1][i] + redlist[2][i])
print("红球预测结果：", redresult)

# 生成蓝球预测结果
blueresult = bluelist[0] + bluelist[1] + bluelist[2]
print("蓝球预测结果：", blueresult)

