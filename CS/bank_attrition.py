import numbers
import random

import numpy as np
import pandas as pd
from matplotlib import pyplot
from numpy import path
from pandas.plotting import scatter_matrix
from scipy.stats import chisquare
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


def NumVarPerf(df, col, target, filepath, truncation=False):
    """
    该代码定义了一个函数 NumVarPerf ，用于生成数值型自变量的直方图。
    函数接受以下参数：
    -  df ：包含数值自变量和因变量的数据集
    -  col ：具有数值型自变量的列名
    -  target ：因变量的列名，取值为0或1
    -  filepath ：保存直方图的文件路径
    -  truncation ：一个布尔值，指示是否需要对异常值进行截断，默认为False
     函数的返回值是描述性统计。
     函数的实现步骤如下：
    1. 从数据集中提取目标变量和特定自变量的有效记录，并存储在 validDf 中。
    2. 计算有效记录的百分比，并将其格式化为百分比字符串。
    3. 计算特定自变量的描述性统计指标，包括均值、标准差、最大值和最小值，并将其格式化为科学计数法字符串。
    4. 根据目标变量将有效记录分为两组，分别存储在变量 x 和 y 中。
    5. 计算每组数据的权重，用于绘制直方图。
    6. 如果需要截断异常值，将 x 和 y 中大于第95个分位数的值截断为第95个分位数。
    7. 创建一个图形对象和坐标轴对象。
    8. 绘制两组数据的直方图，并设置标题和坐标轴标签。
    9. 保存直方图为图片文件。
    10. 关闭图形对象。
    该函数的作用是生成数值型自变量的直方图，并提供相关的描述性统计信息
    """
    # 提取目标变量和特定自变量
    validDf = df.loc[df[col] == df[col]][[col, target]]
    # 有效元素的百分比
    validRcd = validDf.shape[0] * 1.0 / df.shape[0]
    # 将百分比格式设置为percent
    validRcdFmt = "%.2f%%" % (validRcd * 100)
    # 每个数字列的描述性统计
    descStats = validDf[col].describe()
    mu = "%.2e" % descStats['mean']
    std = "%.2e" % descStats['std']
    maxVal = "%.2e" % descStats['max']
    minVal = "%.2e" % descStats['min']
    # 我们用搅拌状态来表示分布
    x = validDf.loc[validDf[target] == 1][col]
    y = validDf.loc[validDf[target] == 0][col]
    xweights = 100.0 * np.ones_like(x) / x.size
    yweights = 100.0 * np.ones_like(y) / y.size
    # 如果需要截断，截断第95个分位数的数字
    if truncation:
        pcnt95 = np.percentile(validDf[col], 95)
        x = x.map(lambda x: min(x, pcnt95))
        y = y.map(lambda x: min(x, pcnt95))
    fig, ax = pyplot.subplots()
    ax.hist(x, weights=xweights, alpha=0.5, label='Attrition')
    ax.hist(y, weights=yweights, alpha=0.5, label='Retained')
    titleText = 'Histogram of ' + col + '\n' + 'valid pcnt =' + validRcdFmt + ', Mean =' + mu + ', Std=' + std + '\n max=' + maxVal + ', min=' + minVal
    ax.set(title=titleText, ylabel='% of Dataset in Bin')
    ax.margins(0.05)
    ax.set_ylim(bottom=0)
    pyplot.legend(loc='upper right')
    figSavePath = filepath + str(col) + '.png'
    pyplot.savefig(figSavePath)
    pyplot.close(1)


def CharVarPerf(df, col, target, filepath):
    """
    这段代码定义了一个名为CharVarPerf的函数，该函数接受四个参数：df（包含数值独立变量和因变量的数据集），col（数值类型的独立变量），target（因变量，取值为0或1的类别），filepath（保存直方图的位置）。函数的返回值是描述性统计。
    函数首先从df中筛选出col列不为空的数据，并保存在validDf中。然后计算validDf的记录数占df记录数的比例，保存在validRcd中。接着，计算validDf的记录数，保存在recdNum中。将validRcd乘以100并格式化为百分数形式，保存在validRcdFmt中。
    接下来，定义两个空字典freqDict和churnRateDict。然后，对validDf[col]中的每个唯一值v进行循环。在循环中，筛选出validDf[col]等于v的数据，并保存在vDf中。计算vDf的记录数占recdNum的比例，并保存在freqDict[v]中。计算vDf中target列的和除以vDf的记录数，并保存在churnRateDict[v]中。
    将freqDict和churnRateDict合并为一个DataFrame，列名分别为'percent'和'churn rate'，保存在descStats中。
    创建一个matplotlib的figure对象fig。然后，创建一个子图ax，并将其添加到fig中。再创建一个共享x轴的子图ax2，并将其添加到fig中。
    设置图表的标题为'col的百分比和流失率\n valid pcnt = validRcdFmt'，其中col为函数参数col的值，validRcdFmt为上面计算得到的validRcdFmt的值。
    在ax上绘制'churn rate'列的折线图，颜色为红色。在ax2上绘制'percent'列的柱状图，颜色为蓝色，柱宽为0.2，位置为1。
    设置ax的y轴标签为'churn rate'，设置ax2的y轴标签为'percentage'。
    将图表保存到figSavePath中，路径为filepath加上col的字符串形式加上'.png'。关闭figure对象。
    最后，函数返回描述性统计descStats。
    """
    validDf = df.loc[df[col] == df[col]][[col, target]]
    validRcd = validDf.shape[0] * 1.0 / df.shape[0]
    recdNum = validDf.shape[0]
    validRcdFmt = "%.2f%%" % (validRcd * 100)
    freqDict = {}
    churnRateDict = {}
    # 对于分类变量中的每个类别，我们计算百分比和流失率
    # for each category in the categorical variable, we count the percentage and churn rate
    for v in set(validDf[col]):
        vDf = validDf.loc[validDf[col] == v]
        freqDict[v] = vDf.shape[0] * 1.0 / recdNum
        churnRateDict[v] = sum(vDf[target]) * 1.0 / vDf.shape[0]
    descStats = pd.DataFrame({'percent': freqDict, 'churn rate': churnRateDict})
    fig = pyplot.figure()  # 创建matplotlib图 Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes 创建matplotlib坐标轴
    ax2 = ax.twinx()  # Create another axes that shares the same x-axis as ax. 创建共享ax x轴的另一个坐标轴
    pyplot.title('The percentage and churn rate for ' + col + '\n valid pcnt =' + validRcdFmt)
    descStats['churn rate'].plot(kind='line', color='red', ax=ax)
    descStats.percent.plot(kind='bar', color='blue', ax=ax2, width=0.2, position=1)
    ax.set_ylabel('churn rate')
    ax2.set_ylabel('percentage')
    figSavePath = filepath + str(col) + '.png'
    pyplot.savefig(figSavePath)
    pyplot.close(1)


# read the data: customer details and dictionary of fields in customer details dataset

#  这段代码的作用是读取两个csv文件，然后将它们合并成一个dataframe，并对合并后的dataframe进行类型检查和基本描述。
#  首先，代码使用pd.read_csv函数从指定路径读取bankChurn.csv和ExternalData.csv两个文件，并将它们分别存储在bankChurn和externalData两个变量中。
#  接下来，代码使用pd.merge函数将bankChurn和externalData两个dataframe根据'CUST_ID'列进行合并，并将合并后的结果存储在AllData变量中。
#  然后，代码定义了一个变量columns，用于存储AllData中的所有列名，并从中移除了'CHURN_CUST_IND'列，因为它是目标变量，不是我们的目标。
#  接着，代码根据列的类型将它们分为数值类型和字符类型。对于每一列，代码首先获取该列的所有唯一值，并将其中的nan值排除。然后，通过判断第一个非nan值的类型，将列分为数值类型和字符类型，并分别存储在numericCols和stringCols两个列表中。
#  最后，代码打印出无法确定类型的列的信息。
#  总结：这段代码的主要作用是读取两个csv文件并合并成一个dataframe，然后对合并后的dataframe进行类型检查和基本描述。
# read the internal data and external data
# 'path' is the path for students' folder which contains the lectures of xiaoxiang
bankChurn = pd.read_csv(path + '/数据/bank attrition/bankChurn.csv', header=0)
externalData = pd.read_csv(path + '/数据/bank attrition/ExternalData.csv', header=0)
# merge two dataframes合并两个数据帧
AllData = pd.merge(bankChurn, externalData, on='CUST_ID')

# step 1: check the type for each column and descripe the basic profile
columns = set(list(AllData.columns))
columns.remove('CHURN_CUST_IND')  # the target variable is not our object
# we differentiate the numerical type and catigorical type of the columns
numericCols = []
stringCols = []
for var in columns:
    x = list(set(AllData[var]))
    x = [i for i in x if i == i]  # we need to eliminate the noise, which is nan type
    if isinstance(x[0], numbers.Real):
        numericCols.append(var)
    elif isinstance(x[0], str):
        stringCols.append(var)
    else:
        print('The type of ', var, ' cannot be determined')

#  这段代码的作用是对数据集中的各个变量进行性能评估，并生成相应的结果图像。
#  首先，代码通过指定文件路径来设置保存结果图像的位置。
#  接下来，使用for循环遍历numericCols中的每个变量，并调用NumVarPerf函数来评估该变量在预测CHURN_CUST_IND（客户流失指标）方面的性能。评估结果会保存在之前指定的文件路径中。
#  然后，代码再次设置文件路径，用于保存处理过的数据集的结果图像。
#  接着，使用for循环遍历numericCols中的每个变量，并调用NumVarPerf函数来评估该变量在预测CHURN_CUST_IND方面的性能。此次评估会对异常值进行截断处理。
#  接下来，代码进行ANOVA（方差分析）测试，并将结果保存在anova_results变量中。该测试用于评估ASSET_MON_AVG_BAL（平均每月资产余额）变量与CHURN_CUST_IND之间的关系。
#  最后，代码再次设置文件路径，用于保存处理过的数据集的结果图像。
#  最后，使用for循环遍历stringCols中的每个变量，并调用CharVarPerf函数来评估该变量在预测CHURN_CUST_IND方面的性能。评估结果会保存在之前指定的文件路径中。
# Part 1: Single factor analysis for independent variables自变量单因素分析
# we check the distribution of each numerical variable, separated by churn/not churn
filepath = path + '/Notes/02 银行业客户流失预警模型的介绍/Pictures1/'
for var in numericCols:
    NumVarPerf(AllData, var, 'CHURN_CUST_IND', filepath)

# need to do some truncation for outliers需要对异常值做一些截断处理
filepath = path + '/Notes/02 银行业客户流失预警模型的介绍/Pictures2/'
for val in numericCols:
    NumVarPerf(AllData, val, 'CHURN_CUST_IND', filepath, True)

# anova test
anova_results = anova_lm(ols('ASSET_MON_AVG_BAL~CHURN_CUST_IND', AllData).fit())

# single factor analysis for categorical analysis
filepath = path + '/Notes/02 银行业客户流失预警模型的介绍/Pictures3/'
for val in stringCols:
    print(val)
    CharVarPerf(AllData, val, 'CHURN_CUST_IND', filepath)

# chisquare test
#   这段代码的功能是进行卡方检验，以确定性别（GENDER）是否对流失客户指标（CHURN_CUST_IND）有显著影响。
#  代码步骤解释：
# 1. 将AllData中的'GENDER_CD'和'CHURN_CUST_IND'列提取出来，赋值给chisqDf。
# 2. 使用chisqDf中的'GENDER_CD'进行分组，计算每个分组中'CHURN_CUST_IND'的数量，保存在count列表中。
# 3. 计算每个分组中'CHURN_CUST_IND'为1（即流失客户）的数量，保存在churn列表中。
# 4. 使用count和churn创建一个名为chisqTable的数据框，其中包含'total'列和'churn'列。
# 5. 在chisqTable中添加一个名为'expected'的列，该列的值通过将'total'列的每个元素乘以0.101并四舍五入得到。
# 6. 使用chisqTable中的'churn'和expected'列，计算每行的卡方值，并将结果保存在chisValList列表中。
# 7. 将chisqValList中的所有元素相加，得到chisqVal。
# 8. 根据卡方分布的自由度（2）和显著性水平（0.05），判断chisqVal是否显著。如果chisqVal大于5.99，则GENDER对CHURN_CUST_IND有显著影响。
# 9. 另外，也可以直接使用chisquare函数进行卡方检验，传入chisqTable的'churn'和'expected'列作为参数。
chisqDf = AllData[['GENDER_CD', 'CHURN_CUST_IND']]
grouped = chisqDf['CHURN_CUST_IND'].groupby(chisqDf['GENDER_CD'])
count = list(grouped.count())
churn = list(grouped.sum())
chisqTable = pd.DataFrame({'total': count, 'churn': churn})
chisqTable['expected'] = chisqTable['total'].map(lambda x: round(x * 0.101))
chisqValList = chisqTable[['churn', 'expected']].apply(lambda x: (x[0] - x[1]) ** 2 / x[1], axis=1)
chisqVal = sum(chisqValList)
# the 2-degree of freedom chisquare under 0.05 is 5.99, which is smaller than chisqVal = 32.66, so GENDER is significant
# Alternatively, we can use function directly或者，我们可以直接使用function
chisquare(chisqTable['churn'], chisqTable['expected'])

#   这段代码的功能是绘制一个散点矩阵图，用于展示数据集中数值型列之间的相关性。
#  代码的步骤如下：
# 1. 创建一个字典 col_to_index，其中键为 numericCols 列表中的元素，值为 'var' + str(i)，这里的 i 是该元素在 numericCols 列表中的索引。
# 2. 从 numericCols 列表中随机选择 15 个列，并将其赋值给 corrCols。
# 3. 从 AllData 数据集中提取 corrCols 列的数据，并将结果赋值给 sampleDf。
# 4. 对于 corrCols 列中的每一列 col，使用 col_to_index 字典将 sampleDf 中的该列重命名为 col_to_index[col]。
# 5. 使用 scatter_matrix 函数绘制 sampleDf 的散点矩阵图，设置透明度为 0.2，图像大小为 (6, 6)，对角线使用核密度估计图。
# Part 1: Multi factor analysis for independent variables自变量多因素分析。
# use short name to replace the raw name, since the raw names are too long to be shown
col_to_index = {numericCols[i]: 'var' + str(i) for i in range(len(numericCols))}
# sample from the list of columns, since too many columns cannot be displayed in the single plot
# 从列列表中采样，因为在单个图中不能显示太多的列
corrCols = random.sample(numericCols, 15)
sampleDf = AllData[corrCols]
for col in corrCols:
    sampleDf.rename(columns={col: col_to_index[col]}, inplace=True)

scatter_matrix(sampleDf, alpha=0.2, figsize=(6, 6), diagonal='kde')
