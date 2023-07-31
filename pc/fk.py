# -*- encoding: gbk -*-
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# 准备数据集，包括企业人员和企业收入等特征
data = {
    '企业人员': [100, 50, 200, 150, 80, 120],
    '企业收入': [1000000, 500000, 2000000, 1500000, 800000, 1200000],
    '风险策划': ['高风险', '低风险', '高风险', '中风险', '低风险', '中风险']
}
df = pd.DataFrame(data)
# 将特征和标签分开
X = df[['企业人员', '企业收入']]
y = df['风险策划']
# 创建决策树模型
model = DecisionTreeClassifier()
# 拟合模型
model.fit(X, y)
# 进行预测
new_data = {
    '企业人员': [120, 80],
    '企业收入': [1300000, 900000]
}
new_df = pd.DataFrame(new_data)
predictions = model.predict(new_df)
# 输出预测结果
for prediction in predictions:
    print(prediction)
