# -*- encoding: gbk -*-
import mysql.connector
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# ׼�����ݼ�������ʹ��һ���򵥵�ʾ������
# ���ݿ�����
mydb = mysql.connector.connect(
    host="localhost",  # ���ݿ�������ַ
    user="root",  # ���ݿ��û���
    passwd="root"  # ���ݿ�����
)

cur = mydb.cursor()

sqlcom = 'select * from gql.runoob_tbl'
df = pd.read_sql(sqlcom, con=mydb)

# �������ͱ�ǩ�ֿ�
X = df[['con_am', 'con_p']]
y = df['con_name']
# ����������ģ��
model = DecisionTreeClassifier()
# ���ģ��
model.fit(X, y)
# ����Ԥ��
new_data = {
    'con_am': [12, 0],
    'con_p': [12, 0]
}
new_df = pd.DataFrame(new_data)
predictions = model.predict(new_df)
# ���Ԥ����
for prediction in predictions:
    print(prediction)
