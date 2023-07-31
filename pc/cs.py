# -*- encoding: gbk -*-
import mysql.connector
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# 准备数据集，这里使用一个简单的示例数据
# 数据库配置
mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root"  # 数据库密码
)

cur = mydb.cursor()

sqlcom = 'select * from gql.runoob_tbl'
df = pd.read_sql(sqlcom, con=mydb)

# 将特征和标签分开
X = df[['con_am', 'con_p']]
y = df['con_name']
# 创建决策树模型
model = DecisionTreeClassifier()
# 拟合模型
model.fit(X, y)
# 进行预测
new_data = {
    'con_am': [12, 0],
    'con_p': [12, 0]
}
new_df = pd.DataFrame(new_data)
predictions = model.predict(new_df)
# 输出预测结果
for prediction in predictions:
    print(prediction)
