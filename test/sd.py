# -*- coding: gbk -*-
import re

pattern = r'^\d[^\W_]{5,251}\d{3}$'
if re.match(pattern, input()):

    print("输入符合要求")
else:
    print("输入不符合要求")
# 测试输入
input1 = "1abcde123"
input2 = "123456789"
input3 = "12@#$5678"
# 输出：输入符合要求
# 输出：输入符合要求
# 输出：输入不符合要求
