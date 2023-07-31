# -*- encoding: gbk -*-
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from requests.auth import HTTPBasicAuth
import os
import xlwings as xw
import re


# ��ȡ�ض���˾��ָ����Ϣ
def get_company_message(company, afterLogin_headers):
    # ��ȡ��ѯ������ҳ���ݣ�ȫ����
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
    # ��ȡ��ҵ��ҳ
    conpany_homePage = details_soup.find_all('div', {'class': 'content'})[0]
    # ��ȡ������Ϣ
    business_message = details_soup.find_all({'table': 'ntable'})[0].text
    # ��ȡ�ɶ���Ϣ
    try:
        partner_message = details_soup.find_all(id=re.compile('partner'))[0].select('table')
        # ����б�Ϊ�գ���������Ϣֻ��vip�˺Ų��ܻ�ȡ������Ϊ0��������
        if partner_message == []:
            partner_message = 0
    except:
        partner_message = 0
        # ��ȡ��Ҫ��Ա
    try:
        main_people = details_soup.find_all(id='mainmember')[0].select('table')
        # ����б�Ϊ�գ���������Ϣֻ��vip�˺Ų��ܻ�ȡ������Ϊ0��������
        if main_people == []:
            main_people = 0
    except:
        main_people = 0
    # ��ȡ����Ͷ��
    try:
        external_touzi = details_soup.find_all(id=re.compile('touzilist'))[0].select('table')
        # ����б�Ϊ�գ���������Ϣֻ��vip�˺Ų��ܻ�ȡ������Ϊ0��������
        if external_touzi == []:
            external_touzi = 0
    except:
        external_touzi = 0
    # ��ȡ�����¼
    try:
        change_record = details_soup.find_all(id=re.compile('changelist'))[0].select('table')
        if change_record == []:
            change_record = 0
    except:
        change_record = 0

    return [target_company, conpany_homePage, business_message, partner_message, main_people, external_touzi,
            change_record]


# ��ȡ��ҵ��ҳͷ������Ϣ
def conpany_homePage_to_df(company_name, company_message):
    if company_message == 0:
        homePage_df = pd.DataFrame()
    else:
        company_content = company_message.find_all('div', {'class': 'contact-info'})[0].text.replace("\n", "").replace(
            " ", "")
        # ����������
        try:
            c1 = company_content.split("���������ˣ�")[1].split('����')[0]
        except:
            c1 = '��'
        # ͳһ������ô���
        try:
            c2 = company_content.split("ͳһ������ô��룺")[1].split("����")[0]
        except:
            c2 = '��'
        # �绰
        c3 = company_content.split("�绰��")[1].split("ͬ�绰")[0].split("����")[0]
        # ����
        c4 = company_content.split("������")[1].split("����")[0]
        # ����
        c5 = company_content.split("���䣺")[1].split("����")[0]
        # ��ַ
        c6 = company_content.split("��ַ��")[1].split("������ҵ")[0]
        # ���
        c7 = company_content.split("��飺")[1].split("����")[0]

        homePage_df = pd.DataFrame({'��˾����': [company_name], '����������': [c1], 'ͳһ������ô���': [c2],
                                    '�绰': [c3], '����': [c4], '����': [c5], '��ַ': [c6], '���': [c7]})

    return homePage_df


# ��ȡ������Ϣ�Ŀ�Ƭ
def business_message_to_df(message):
    # ͳһ������ô���
    unified_social_credit_code = []
    try:
        unified_social_credit_code.append(
            message.split('ͳһ������ô���')[1].split('����')[0].replace(" ", "").replace("\n", ""))
    except:
        unified_social_credit_code.append('�޷��ռ�')
    # ��ҵ����
    list_companys = []
    try:
        list_companys.append(message.split('��ҵ����')[1].split('����')[0].replace(" ", "").replace("\n", ""))
    except:
        list_companys.append('�޷��ռ�')
    # ����������
    Legal_Person = []
    try:
        Legal_Person.append(message.split('����������')[1].split('����')[0].replace("\n", "").replace(" ", ""))
    except:
        Legal_Person.append('�޷��ռ�')
    # �Ǽ�״̬
    Registration_status = []
    try:
        Registration_status.append(message.split('�Ǽ�״̬')[1].split('��������')[0].replace(" ", "").replace("\n", ""))
    except:
        Registration_status.append('�޷��ռ�')
    # ��������
    Date_of_Establishment = []
    try:
        Date_of_Establishment.append(
            message.split('��������')[1].split('ע���ʱ�')[0].replace(" ", "").replace("\n", ""))
    except:
        Date_of_Establishment.append('�޷��ռ�')
    # ע���ʱ�
    registered_capital = []
    try:
        registered_capital.append(message.split('ע���ʱ�')[1].split('ʵ���ʱ�')[0].replace(' ', '').replace("\n", ""))
    except:
        registered_capital.append('�޷��ռ�')
    # ʵ���ʱ�
    contributed_capital = []
    try:
        contributed_capital.append(message.split('ʵ���ʱ�')[1].split('��׼����')[0].replace(' ', '').replace('\n', ''))
    except:
        contributed_capital.append('�޷��ռ�')
    # ��׼����
    Approved_date = []
    try:
        Approved_date.append(message.split('��׼����')[1].split('��֯��������')[0].replace(' ', '').replace("\n", ""))
    except:
        Approved_date.append('�޷��ռ�')
    # ��֯��������
    Organization_Code = []
    try:
        Organization_Code.append(message.split('��֯��������')[1].split('����')[0].replace(' ', '').replace("\n", ""))
    except:
        Organization_Code.append('�޷��ռ�')
    # ����ע���
    companyNo = []
    try:
        companyNo.append(message.split('����ע���')[1].split('����')[0].replace(' ', '').replace("\n", ""))
    except:
        companyNo.append('�޷��ռ�')
    # ��˰��ʶ���
    Taxpayer_Identification_Number = []
    try:
        Taxpayer_Identification_Number.append(
            message.split('��˰��ʶ���')[1].split('����')[0].replace(' ', '').replace("\n", ""))
    except:
        Taxpayer_Identification_Number.append('�޷��ռ�')
    # ��ҵ����
    enterprise_type = []
    try:
        enterprise_type.append(message.split('��ҵ����')[1].split('Ӫҵ����')[0].replace('\n', '').replace(' ', ''))
    except:
        enterprise_type.append('�޷��ռ�')
    # Ӫҵ����
    Business_Term = []
    try:
        Business_Term.append(message.split('Ӫҵ����')[1].split('��˰������')[0].replace('\n', '').replace(' ', ''))
    except:
        Business_Term.append('�޷��ռ�')
    # ��˰������
    Taxpayer_aptitude = []
    try:
        Taxpayer_aptitude.append(message.split('��˰������')[1].split('������ҵ')[0].replace(' ', '').replace("\n", ""))
    except:
        Taxpayer_aptitude.append('�޷��ռ�')
    # ������ҵ
    sub_Industry = []
    try:
        sub_Industry.append(message.split('������ҵ')[1].split('��������')[0].replace('\n', '').replace(' ', ''))
    except:
        sub_Industry.append('�޷��ռ�')
        # ��������
    sub_area = []
    try:
        sub_area.append(message.split('��������')[1].split('�Ǽǻ���')[0].replace(' ', '').replace("\n", ""))
    except:
        sub_area.append('�޷��ռ�')
    # �Ǽǻ���
    Registration_Authority = []
    try:
        Registration_Authority.append(
            message.split('�Ǽǻ���')[1].split('��Ա��ģ')[0].replace(' ', '').replace("\n", ""))
    except:
        Registration_Authority.append('�޷��ռ�')
    # ��Ա��ģ
    staff_size = []
    try:
        staff_size.append(message.split('��Ա��ģ')[1].split('�α�����')[0].replace(' ', '').replace('\n', ''))
    except:
        staff_size.append('�޷��ռ�')
    # �α�����
    Number_of_participants = []
    try:
        Number_of_participants.append(
            message.split('�α�����')[1].split('����ͼ')[0].replace(' ', '').replace("\n", ""))
    except:
        Number_of_participants.append('�޷��ռ�')
    # ������
    Used_Name = []
    try:
        Used_Name.append(message.split('������')[1].split('Ӣ����')[0].replace(' ', '').replace("\n", ""))
    except:
        Used_Name.append('�޷��ռ�')
    # Ӣ����
    English_name = []
    try:
        English_name.append(message.split('Ӣ����')[1].split('��������ҵ����')[0].replace('\n', '').replace(' ', ''))
    except:
        English_name.append('�޷��ռ�')
    # ��������ҵ����
    import_and_export_code = []
    try:
        import_and_export_code.append(
            message.split('��������ҵ����')[1].split('����')[0].replace(' ', '').replace("\n", ""))
    except:
        import_and_export_code.append('�޷��ռ�')
    # ע���ַ
    register_adress = []
    try:
        register_adress.append(message.split('ע���ַ')[1].split('������ҵ')[0].replace(' ', '').replace("\n", ""))
    except:
        register_adress.append('�޷��ռ�')
    # ��Ӫ��Χ
    Business_Scope = []
    try:
        Business_Scope.append(message.split('��Ӫ��Χ')[1].replace(' ', '').replace("\n", ""))
    except:
        Business_Scope.append('�޷��ռ�')
    df = pd.DataFrame(
        {'ͳһ������ô���': unified_social_credit_code, '��ҵ����': list_companys, '����������': Legal_Person,
         '�Ǽ�״̬': Registration_status, '��������': Date_of_Establishment, 'ע���ʱ�': registered_capital,
         'ʵ���ʱ�': contributed_capital, '��׼����': Approved_date, '��֯��������': Organization_Code,
         '����ע���': companyNo, '��˰��ʶ���': Taxpayer_Identification_Number, '��ҵ����': enterprise_type,
         'Ӫҵ����': Business_Term, '��˰������': Taxpayer_aptitude,
         '������ҵ': sub_Industry, '��������': sub_area, '�Ǽǻ���': Registration_Authority, '��Ա��ģ': staff_size,
         '�α�����': Number_of_participants, '������': Used_Name, 'Ӣ����': English_name,
         '��������ҵ����': import_and_export_code,
         'ע���ַ': register_adress, '��Ӫ��Χ': Business_Scope})

    return df


# ��ȡ����Ϊ����Ŀ�Ƭ��Ϣ
def col_is_vertical_to_df(company_name, message):
    if message == 0:
        col_df = pd.DataFrame()
    else:
        # ��λ����Ҫ���Ǹ���񣬿�id=�ض�id��Ȼ����������������ҵ�table��ǩ
        list_col = []
        list_row_all = []
        # ��ȡ����
        col_name = message[0].select('tr')[0].select('th')
        for i in range(len(col_name)):
            list_col.append(col_name[i].text.replace(' ', '').replace('\n', ''))
        # ��ȡÿһ�е���Ϣ
        row = len(message[0].select('tr')) - 1
        for i in range(row):
            list_row = []
            col_i = message[0].select('tr')[i + 1].select('td')
            for i in range(len(col_i)):
                list_row.append(col_i[i].text.replace(' ', '').replace('\n', '').split('����')[0])
            list_row_all.append(list_row)
        # ����Ϊdataframe
        col_df = pd.DataFrame(list_row_all, columns=list_col)
        col_df['��˾����'] = company_name
    return col_df


# �����й���Ĺ̶��У�����ר�ŵĴ�����
def regular_line(app, sheet_name, df):
    if len(df) == 0:
        pass
    else:
        # ����Ӧ�������������
        sheet = app.sheets[sheet_name]

        # ��ȡ������Ŀǰ����
        if sheet.used_range.rows.count == 1:
            now_row = sheet.used_range.rows.count
            # ��dataframe������д��xlsx
            sheet.range('A' + str(now_row)).options(pd.DataFrame, expand='table', index=False).value = df
            sheet.range('A1').expand('right').api.Font.Bold = True
        else:
            now_row = sheet.used_range.rows.count + 1
            # ��dataframe������д��xlsx
            sheet.range('A' + str(now_row)).options(pd.DataFrame, expand='table', header=False, index=False).value = df


# �����޹���Ĺ̶��У�����ר�ŵĴ�����
def Irregular_line(app, sheet_name, df):
    if len(df) == 0:
        pass
    else:
        # ����Ӧ�������������
        sheet = app.sheets[sheet_name]

        # ��ȡ������Ŀǰ����
        if sheet.used_range.rows.count == 1:
            now_row = sheet.used_range.rows.count
        else:
            now_row = sheet.used_range.rows.count + 2
        # ��dataframe������д��xlsx
        sheet.range('A' + str(now_row)).options(pd.DataFrame, expand='table', index=False).value = df

        # ��������һ���ϻ�ɫ��Ȼ���������ϻ�ɫ
        for i in range(len(df2) + 1):
            if i == 0:
                sheet.range('A' + str(now_row)).expand('right').color = (255, 255, 0)
            else:
                sheet.range('A' + str(now_row + i)).expand('right').api.Font.Color = 0x00000
                sheet.range('A' + str(now_row + i)).expand('right').color = (220, 220, 220)
                print('A' + str(now_row + i))


# ������ΪͼƬ�����յ�ԭ��������ظ������������ȥ�أ��˺���ֻ�ʺ��ڴ󲿷����
def dedup_name(origin_name):  # origin_nameΪԭʼ������
    global target_name
    if len(origin_name) >= 2:
        if origin_name[0:1] == origin_name[1:2]:
            target_name = origin_name[1:]
        else:
            target_name = origin_name
    target_name = target_name.replace('����������', '').replace('ʵ�ʿ�����', '').replace('��ɶ�', '').replace(
        '������', '').replace('������', '')

    return target_name


# �޸���Щ�����������ñ�����
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
save_path = 'C:/Users/18339/Desktop/ĳĳ.csv'

# ��������
companys = ['��������Ѷ�����ϵͳ���޹�˾', '����Ͱͣ��й������޹�˾']
if __name__ == '__main__':
    # ���ֻỰ
    # �½�һ��session����
    sess = requests.session()

    # ���headers��headerΪ�Լ���¼��������ַ�������˺������¼֮������ʾ��header���˴�����Ϸ������˻�ȡ������
    afterLogin_headers = {'User-Agent': user_agent, 'cookie': cookie}

    # ���û��������֤,�������ִ�в�ѯָ��
    res = requests.get('https://www.qcc.com/', headers=afterLogin_headers, auth=HTTPBasicAuth(username, password))
    print(res.status_code)

    # ��ȡ�б��е�ÿһ����˾����Ϣ
    app = xw.App(visible=False)
    try:
        for i in range(len(companys)):

            # ��ȡ�ù�˾�Ĳ�����ҳ��Ϣ
            company_message = get_company_message(companys[i], afterLogin_headers)
            # ��ҵ��ҳ
            df1 = conpany_homePage_to_df(company_message[0], company_message[1])
            # ������Ϣ
            df2 = business_message_to_df(company_message[2])
            df2['����������'] = df2['����������'].apply(dedup_name)
            # �ɶ���Ϣ
            df3 = col_is_vertical_to_df(company_message[0], company_message[3])
            # ��Ҫ��Ա
            df4 = col_is_vertical_to_df(company_message[0], company_message[4])
            df4['����'] = df4['����'].apply(dedup_name)
            # ����Ͷ��
            df5 = col_is_vertical_to_df(company_message[0], company_message[5])
            # �����¼
            df6 = col_is_vertical_to_df(company_message[0], company_message[6])

            # ���Ŀ��xlsx�Ƿ���ڣ�����������ǰ������
            if not os.path.exists(save_path):
                workbook = app.books.add()
                workbook.save(save_path)
                workbook.close()
                time.sleep(1)

                # �մ�����ʱ���ǿ��ļ�����������������Ӧ���������е�һ��д��
                wb = app.books.open(save_path)
                wb.sheets[0].name = wb.sheets[0].name.replace('Sheet1', '��ҵ��ҳ')
                wb.sheets.add('������Ϣ', after='��ҵ��ҳ')
                wb.sheets.add('�ɶ���Ϣ', after='������Ϣ')
                wb.sheets.add('��Ҫ��Ա', after='�ɶ���Ϣ')
                wb.sheets.add('����Ͷ��', after='��Ҫ��Ա')
                wb.sheets.add('�����¼', after='����Ͷ��')
                wb.save()
                wb.close()

            # д���ݽ�xlxs
            wb_write = app.books.open(save_path)
            regular_line(wb_write, '��ҵ��ҳ', df1)
            regular_line(wb_write, '������Ϣ', df2)
            Irregular_line(wb_write, '�ɶ���Ϣ', df3)
            Irregular_line(wb_write, '��Ҫ��Ա', df4)
            Irregular_line(wb_write, '����Ͷ��', df5)
            Irregular_line(wb_write, '�����¼', df6)
            wb_write.save()
            wb_write.close()
            time.sleep(1)

        app.quit()
    except Exception as e:
        app.quit()
        print(e)
