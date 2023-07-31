# -*- encoding: gbk -*-
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from requests.auth import HTTPBasicAuth
import os
import xlwings as xw
import re


# 获取特定公司的指定信息
def get_company_message(company, afterLogin_headers):
    # 获取查询到的网页内容（全部）
    search = sess.get('https://www.qcc.com/web/search?key={}'.format(company), headers=afterLogin_headers, timeout=10)
    search.raise_for_status()
    search.encoding = 'utf-8'  # linux utf-8
    soup = BeautifulSoup(search.text, features="html.parser")
    href = soup.find_all('a', {'class': 'title'})[0].get('href')
    target_company = soup.find_all('a', {'class': 'title'})[0].text
    time.sleep(4)
    details = sess.get(href, headers=afterLogin_headers, timeout=10)
    details.raise_for_status()
    details.encoding = 'utf-8'  # linux utf-8
    details_soup = BeautifulSoup(details.text, features="html.parser")
    # 获取企业主页
    conpany_homePage = details_soup.find_all('div', {'class': 'content'})[0]
    # 获取工商信息
    business_message = details_soup.find_all({'table': 'ntable'})[0].text
    # 获取股东信息
    try:
        partner_message = details_soup.find_all(id=re.compile('partner'))[0].select('table')
        # 如果列表为空，则代表改信息只有vip账号才能获取，设置为0跳过处理
        if partner_message == []:
            partner_message = 0
    except:
        partner_message = 0
        # 获取主要人员
    try:
        main_people = details_soup.find_all(id='mainmember')[0].select('table')
        # 如果列表为空，则代表改信息只有vip账号才能获取，设置为0跳过处理
        if main_people == []:
            main_people = 0
    except:
        main_people = 0
    # 获取对外投资
    try:
        external_touzi = details_soup.find_all(id=re.compile('touzilist'))[0].select('table')
        # 如果列表为空，则代表改信息只有vip账号才能获取，设置为0跳过处理
        if external_touzi == []:
            external_touzi = 0
    except:
        external_touzi = 0
    # 获取变更记录
    try:
        change_record = details_soup.find_all(id=re.compile('changelist'))[0].select('table')
        if change_record == []:
            change_record = 0
    except:
        change_record = 0

    return [target_company, conpany_homePage, business_message, partner_message, main_people, external_touzi,
            change_record]


# 获取企业主页头部的信息
def conpany_homePage_to_df(company_name, company_message):
    if company_message == 0:
        homePage_df = pd.DataFrame()
    else:
        company_content = company_message.find_all('div', {'class': 'contact-info'})[0].text.replace("\n", "").replace(
            " ", "")
        # 法定代表人
        try:
            c1 = company_content.split("法定代表人：")[1].split('关联')[0]
        except:
            c1 = '无'
        # 统一社会信用代码
        try:
            c2 = company_content.split("统一社会信用代码：")[1].split("复制")[0]
        except:
            c2 = '无'
        # 电话
        c3 = company_content.split("电话：")[1].split("同电话")[0].split("更多")[0]
        # 官网
        c4 = company_content.split("官网：")[1].split("邮箱")[0]
        # 邮箱
        c5 = company_content.split("邮箱：")[1].split("复制")[0]
        # 地址
        c6 = company_content.split("地址：")[1].split("附近企业")[0]
        # 简介
        c7 = company_content.split("简介：")[1].split("复制")[0]

        homePage_df = pd.DataFrame({'公司名称': [company_name], '法定代表人': [c1], '统一社会信用代码': [c2],
                                    '电话': [c3], '官网': [c4], '邮箱': [c5], '地址': [c6], '简介': [c7]})

    return homePage_df


# 获取工商信息的卡片
def business_message_to_df(message):
    # 统一社会信用代码
    unified_social_credit_code = []
    try:
        unified_social_credit_code.append(
            message.split('统一社会信用代码')[1].split('复制')[0].replace(" ", "").replace("\n", ""))
    except:
        unified_social_credit_code.append('无法收集')
    # 企业名称
    list_companys = []
    try:
        list_companys.append(message.split('企业名称')[1].split('复制')[0].replace(" ", "").replace("\n", ""))
    except:
        list_companys.append('无法收集')
    # 法定代表人
    Legal_Person = []
    try:
        Legal_Person.append(message.split('法定代表人')[1].split('关联')[0].replace("\n", "").replace(" ", ""))
    except:
        Legal_Person.append('无法收集')
    # 登记状态
    Registration_status = []
    try:
        Registration_status.append(message.split('登记状态')[1].split('成立日期')[0].replace(" ", "").replace("\n", ""))
    except:
        Registration_status.append('无法收集')
    # 成立日期
    Date_of_Establishment = []
    try:
        Date_of_Establishment.append(
            message.split('成立日期')[1].split('注册资本')[0].replace(" ", "").replace("\n", ""))
    except:
        Date_of_Establishment.append('无法收集')
    # 注册资本
    registered_capital = []
    try:
        registered_capital.append(message.split('注册资本')[1].split('实缴资本')[0].replace(' ', '').replace("\n", ""))
    except:
        registered_capital.append('无法收集')
    # 实缴资本
    contributed_capital = []
    try:
        contributed_capital.append(message.split('实缴资本')[1].split('核准日期')[0].replace(' ', '').replace('\n', ''))
    except:
        contributed_capital.append('无法收集')
    # 核准日期
    Approved_date = []
    try:
        Approved_date.append(message.split('核准日期')[1].split('组织机构代码')[0].replace(' ', '').replace("\n", ""))
    except:
        Approved_date.append('无法收集')
    # 组织机构代码
    Organization_Code = []
    try:
        Organization_Code.append(message.split('组织机构代码')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        Organization_Code.append('无法收集')
    # 工商注册号
    companyNo = []
    try:
        companyNo.append(message.split('工商注册号')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        companyNo.append('无法收集')
    # 纳税人识别号
    Taxpayer_Identification_Number = []
    try:
        Taxpayer_Identification_Number.append(
            message.split('纳税人识别号')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        Taxpayer_Identification_Number.append('无法收集')
    # 企业类型
    enterprise_type = []
    try:
        enterprise_type.append(message.split('企业类型')[1].split('营业期限')[0].replace('\n', '').replace(' ', ''))
    except:
        enterprise_type.append('无法收集')
    # 营业期限
    Business_Term = []
    try:
        Business_Term.append(message.split('营业期限')[1].split('纳税人资质')[0].replace('\n', '').replace(' ', ''))
    except:
        Business_Term.append('无法收集')
    # 纳税人资质
    Taxpayer_aptitude = []
    try:
        Taxpayer_aptitude.append(message.split('纳税人资质')[1].split('所属行业')[0].replace(' ', '').replace("\n", ""))
    except:
        Taxpayer_aptitude.append('无法收集')
    # 所属行业
    sub_Industry = []
    try:
        sub_Industry.append(message.split('所属行业')[1].split('所属地区')[0].replace('\n', '').replace(' ', ''))
    except:
        sub_Industry.append('无法收集')
        # 所属地区
    sub_area = []
    try:
        sub_area.append(message.split('所属地区')[1].split('登记机关')[0].replace(' ', '').replace("\n", ""))
    except:
        sub_area.append('无法收集')
    # 登记机关
    Registration_Authority = []
    try:
        Registration_Authority.append(
            message.split('登记机关')[1].split('人员规模')[0].replace(' ', '').replace("\n", ""))
    except:
        Registration_Authority.append('无法收集')
    # 人员规模
    staff_size = []
    try:
        staff_size.append(message.split('人员规模')[1].split('参保人数')[0].replace(' ', '').replace('\n', ''))
    except:
        staff_size.append('无法收集')
    # 参保人数
    Number_of_participants = []
    try:
        Number_of_participants.append(
            message.split('参保人数')[1].split('趋势图')[0].replace(' ', '').replace("\n", ""))
    except:
        Number_of_participants.append('无法收集')
    # 曾用名
    Used_Name = []
    try:
        Used_Name.append(message.split('曾用名')[1].split('英文名')[0].replace(' ', '').replace("\n", ""))
    except:
        Used_Name.append('无法收集')
    # 英文名
    English_name = []
    try:
        English_name.append(message.split('英文名')[1].split('进出口企业代码')[0].replace('\n', '').replace(' ', ''))
    except:
        English_name.append('无法收集')
    # 进出口企业代码
    import_and_export_code = []
    try:
        import_and_export_code.append(
            message.split('进出口企业代码')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        import_and_export_code.append('无法收集')
    # 注册地址
    register_adress = []
    try:
        register_adress.append(message.split('注册地址')[1].split('附近企业')[0].replace(' ', '').replace("\n", ""))
    except:
        register_adress.append('无法收集')
    # 经营范围
    Business_Scope = []
    try:
        Business_Scope.append(message.split('经营范围')[1].replace(' ', '').replace("\n", ""))
    except:
        Business_Scope.append('无法收集')
    df = pd.DataFrame(
        {'统一社会信用代码': unified_social_credit_code, '企业名称': list_companys, '法定代表人': Legal_Person,
         '登记状态': Registration_status, '成立日期': Date_of_Establishment, '注册资本': registered_capital,
         '实缴资本': contributed_capital, '核准日期': Approved_date, '组织机构代码': Organization_Code,
         '工商注册号': companyNo, '纳税人识别号': Taxpayer_Identification_Number, '企业类型': enterprise_type,
         '营业期限': Business_Term, '纳税人资质': Taxpayer_aptitude,
         '所属行业': sub_Industry, '所属地区': sub_area, '登记机关': Registration_Authority, '人员规模': staff_size,
         '参保人数': Number_of_participants, '曾用名': Used_Name, '英文名': English_name,
         '进出口企业代码': import_and_export_code,
         '注册地址': register_adress, '经营范围': Business_Scope})

    return df


# 获取列名为横向的卡片信息
def col_is_vertical_to_df(company_name, message):
    if message == 0:
        col_df = pd.DataFrame()
    else:
        # 定位到你要的那个表格，靠id=特定id，然后再在这个基础上找到table标签
        list_col = []
        list_row_all = []
        # 获取列名
        col_name = message[0].select('tr')[0].select('th')
        for i in range(len(col_name)):
            list_col.append(col_name[i].text.replace(' ', '').replace('\n', ''))
        # 获取每一行的信息
        row = len(message[0].select('tr')) - 1
        for i in range(row):
            list_row = []
            col_i = message[0].select('tr')[i + 1].select('td')
            for i in range(len(col_i)):
                list_row.append(col_i[i].text.replace(' ', '').replace('\n', '').split('关联')[0])
            list_row_all.append(list_row)
        # 汇总为dataframe
        col_df = pd.DataFrame(list_row_all, columns=list_col)
        col_df['公司名称'] = company_name
    return col_df


# 对于有规则的固定列，授予专门的处理函数
def regular_line(app, sheet_name, df):
    if len(df) == 0:
        pass
    else:
        # 给对应工作表添加内容
        sheet = app.sheets[sheet_name]

        # 获取工作表目前的行
        if sheet.used_range.rows.count == 1:
            now_row = sheet.used_range.rows.count
            # 将dataframe的数据写进xlsx
            sheet.range('A' + str(now_row)).options(pd.DataFrame, expand='table', index=False).value = df
            sheet.range('A1').expand('right').api.Font.Bold = True
        else:
            now_row = sheet.used_range.rows.count + 1
            # 将dataframe的数据写进xlsx
            sheet.range('A' + str(now_row)).options(pd.DataFrame, expand='table', header=False, index=False).value = df


# 对于无规则的固定列，授予专门的处理函数
def Irregular_line(app, sheet_name, df):
    if len(df) == 0:
        pass
    else:
        # 给对应工作表添加内容
        sheet = app.sheets[sheet_name]

        # 获取工作表目前的行
        if sheet.used_range.rows.count == 1:
            now_row = sheet.used_range.rows.count
        else:
            now_row = sheet.used_range.rows.count + 2
        # 将dataframe的数据写进xlsx
        sheet.range('A' + str(now_row)).options(pd.DataFrame, expand='table', index=False).value = df

        # 将列名那一行上黄色，然后数据行上灰色
        for i in range(len(df2) + 1):
            if i == 0:
                sheet.range('A' + str(now_row)).expand('right').color = (255, 255, 0)
            else:
                sheet.range('A' + str(now_row + i)).expand('right').api.Font.Color = 0x00000
                sheet.range('A' + str(now_row + i)).expand('right').color = (220, 220, 220)
                print('A' + str(now_row + i))


# 对于因为图片带有姓的原因造成姓重复的情况，进行去重，此函数只适合于大部分情况
def dedup_name(origin_name):  # origin_name为原始的名字
    global target_name
    if len(origin_name) >= 2:
        if origin_name[0:1] == origin_name[1:2]:
            target_name = origin_name[1:]
        else:
            target_name = origin_name
    target_name = target_name.replace('最终受益人', '').replace('实际控制人', '').replace('大股东', '').replace(
        '有限制', '').replace('高消费', '')

    return target_name


# 修改这些参数即可运用本案例
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/114.0.0.0 Mobile Safari/537.36'
cookie = 'jsid=SEO-BAIDU-ALL-SY-000001; TYCID=8a6bc6d0244011ee9749f1239144b0ce; sajssdk_2015_cross_new_user=1; ' \
         'Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1689557012; bannerFlag=true; ' \
         'RTYCID=58f786daa3ed42bfbac55e6baf461ceb; ssuid=2348343041; _ga=GA1.2.1484384026.1689559318; ' \
         '_gid=GA1.2.136949336.1689559318; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2241492493%22%2C' \
         '%22first_id%22%3A%2218961720d331009-0c98f7c860143a-26031d51-1327104-18961720d348b8%22%2C%22props%22%3A%7B' \
         '%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22' \
         '%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A' \
         '%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22identities%22%3A' \
         '%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg5NjE3MjBkMzMxMDA5LTBjOThmN2M4NjAxNDNhLTI2MDMxZDUxLTEzMjcxMDQtMTg5NjE3MjBkMzQ4YjgiLCIkaWRlbnRpdHlfbG9naW5faWQiOiI0MTQ5MjQ5MyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2241492493%22%7D%2C%22%24device_id%22%3A%2218961720d331009-0c98f7c860143a-26031d51-1327104-18961720d348b8%22%7D; HWWAFSESID=69463217aa394ea894f; HWWAFSESTIME=1689559987302; csrfToken=QnPEi5-57Kz6jEgpI-V_ArlY; Hm_lvt_d5ceb643638c8ee5fbf79d207b00f07e=1689559995; Hm_lpvt_d5ceb643638c8ee5fbf79d207b00f07e=1689560057; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1689560100; tyc-user-info={%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2218531151887%22}; tyc-user-info-save-time=1689560978930; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUzMTE1MTg4NyIsImlhdCI6MTY4OTU2MDk3OCwiZXhwIjoxNjkyMTUyOTc4fQ.1aDNC59YtTRg2zVwmCGxchpV_mqCarZhOmNPmq9b4AoeucCtnDCRw2TmAwGjNL96uCWeU3DlBa4Sc-TOfNZV3g; tyc-user-phone=%255B%252218531151887%2522%255D; searchSessionId=1689561059.80447277; _gat_gtag_UA_123487620_1=1'
username = '18531151887'
password = 'Gao823624'
save_path = 'C:/Users/18339/Desktop/某某.csv'

# 测试所用
companys = ['深圳市腾讯计算机系统有限公司', '阿里巴巴（中国）有限公司']
if __name__ == '__main__':
    # 保持会话
    # 新建一个session对象
    sess = requests.session()

    # 添加headers（header为自己登录的企查查网址，输入账号密码登录之后所显示的header，此代码的上方介绍了获取方法）
    afterLogin_headers = {'User-Agent': user_agent, 'cookie': cookie}

    # 以用户的身份认证,方便后面执行查询指令
    res = requests.get('https://www.qcc.com/', headers=afterLogin_headers, auth=HTTPBasicAuth(username, password))
    print(res.status_code)

    # 获取列表中的每一个公司的信息
    app = xw.App(visible=False)
    try:
        for i in range(len(companys)):

            # 获取该公司的部分网页信息
            company_message = get_company_message(companys[i], afterLogin_headers)
            # 企业主页
            df1 = conpany_homePage_to_df(company_message[0], company_message[1])
            # 工商信息
            df2 = business_message_to_df(company_message[2])
            df2['法定代表人'] = df2['法定代表人'].apply(dedup_name)
            # 股东信息
            df3 = col_is_vertical_to_df(company_message[0], company_message[3])
            # 主要人员
            df4 = col_is_vertical_to_df(company_message[0], company_message[4])
            df4['姓名'] = df4['姓名'].apply(dedup_name)
            # 对外投资
            df5 = col_is_vertical_to_df(company_message[0], company_message[5])
            # 变更记录
            df6 = col_is_vertical_to_df(company_message[0], company_message[6])

            # 检查目标xlsx是否存在，不存在则提前创建好
            if not os.path.exists(save_path):
                workbook = app.books.add()
                workbook.save(save_path)
                workbook.close()
                time.sleep(1)

                # 刚创建的时候，是空文件，重命名或新增对应工作表，进行第一次写入
                wb = app.books.open(save_path)
                wb.sheets[0].name = wb.sheets[0].name.replace('Sheet1', '企业主页')
                wb.sheets.add('工商信息', after='企业主页')
                wb.sheets.add('股东信息', after='工商信息')
                wb.sheets.add('主要人员', after='股东信息')
                wb.sheets.add('对外投资', after='主要人员')
                wb.sheets.add('变更记录', after='对外投资')
                wb.save()
                wb.close()

            # 写数据进xlxs
            wb_write = app.books.open(save_path)
            regular_line(wb_write, '企业主页', df1)
            regular_line(wb_write, '工商信息', df2)
            Irregular_line(wb_write, '股东信息', df3)
            Irregular_line(wb_write, '主要人员', df4)
            Irregular_line(wb_write, '对外投资', df5)
            Irregular_line(wb_write, '变更记录', df6)
            wb_write.save()
            wb_write.close()
            time.sleep(1)

        app.quit()
    except Exception as e:
        app.quit()
        print(e)
