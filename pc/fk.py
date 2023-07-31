# -*- encoding: gbk -*-
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# ׼�����ݼ���������ҵ��Ա����ҵ���������
data = {
    '��ҵ��Ա': [100, 50, 200, 150, 80, 120],
    '��ҵ����': [1000000, 500000, 2000000, 1500000, 800000, 1200000],
    '���ղ߻�': ['�߷���', '�ͷ���', '�߷���', '�з���', '�ͷ���', '�з���']
}
df = pd.DataFrame(data)
# �������ͱ�ǩ�ֿ�
X = df[['��ҵ��Ա', '��ҵ����']]
y = df['���ղ߻�']
# ����������ģ��
model = DecisionTreeClassifier()
# ���ģ��
model.fit(X, y)
# ����Ԥ��
new_data = {
    '��ҵ��Ա': [120, 80],
    '��ҵ����': [1300000, 900000]
}
new_df = pd.DataFrame(new_data)
predictions = model.predict(new_df)
# ���Ԥ����
for prediction in predictions:
    print(prediction)
