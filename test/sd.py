# -*- coding: gbk -*-
import re

pattern = r'^\d[^\W_]{5,251}\d{3}$'
if re.match(pattern, input()):

    print("�������Ҫ��")
else:
    print("���벻����Ҫ��")
# ��������
input1 = "1abcde123"
input2 = "123456789"
input3 = "12@#$5678"
# ������������Ҫ��
# ������������Ҫ��
# ��������벻����Ҫ��
