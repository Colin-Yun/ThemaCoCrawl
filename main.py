import requests
from bs4 import BeautifulSoup as bs
from usr_class.usr_class import *
from usr_api.usr_api import *
from selenium import webdriver

import pandas as pd
import os
from datetime import date

#chrome_path = "C:\Program Files\Google\Chrome\Application\chromedriver"
chrome_path = "C:\Program Files\Google\Chrome\Application\chromedriver\chromedriver.exe"
thema_page = """https://finance.naver.com/sise/theme.nhn?&page={0}"""
NAVI_PAGE_NUM = 6
col_lab_1 = ["테마", "기업명", "편입사유", "시가총액(억)", "매출액(억)", "영업이익(억)", "영업이익률(%)", "영업이익증가율(%)", "외국인비중(%)", "PER"]

'''************************************************
* @Function Name : get_page
************************************************'''
def get_page(url):
    with requests.Session() as sess:
        page = sess.get(url, verify=False)
        html = page.text
    return html


'''************************************************
* @Function Name : get_thema_url
************************************************'''
def get_thema_url(html):
    soup = bs(html, 'html.parser')
    soup = soup.findAll('td', {'class': 'col_type1'})

    lst = []
    for se in soup:
        tag_info = se.find('a')
        thema_url = tag_info.attrs['href']
        thema_name = tag_info.get_text()
        thema_url = 'https://finance.naver.com' + thema_url

        lst.append(ThemaInfo(thema_url, thema_name))

    return lst


'''************************************************
* @Function Name : proc_get_thema
************************************************'''
def proc_get_thema():
    ret_lst = []
    for i in range(0, NAVI_PAGE_NUM + 1):
        html = get_page(thema_page.format(i))
        res_lst = get_thema_url(html)

        for el in res_lst:
            ret_lst.append(el)

    return ret_lst


'''************************************************
* @Function Name : get_page_selenium
************************************************'''
def get_page_selenium(url, driver):
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/div/a[2]/img').click()                                         #초기항목으로 리셋
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[1]/td[1]/label').click()                        #거래량체크해제
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[1]/td[2]/label').click()                        #매수호가 체크해제
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[1]/td[3]/label').click()                        #거래대금 체크해제
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[2]/td[2]/label').click()                        #매도호가 체크해제
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[2]/td[3]/label').click()                        #전일거래량 체크해제
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[1]/td[4]/label').click()                        #시가총액 체크

    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[1]/td[5]/label').click()                        #영억이익(억) 체크
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[1]/td[6]/label').click()                        #PER 체크
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[2]/td[5]/label').click()                        #영업이익증가율 체크
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[3]/td[3]/label').click()                        #외국인비율 체크
    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/table/tbody/tr[4]/td[4]/label').click()                        #매출액(억) 체크

    driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/form/div/div/div/a[1]/img').click()                                         #적용하기 체크
    html = driver.page_source

    return html


'''************************************************
* @Function Name : proc_get_coinfo
************************************************'''
def proc_get_coinfo(themas):
    driver = webdriver.Chrome(chrome_path, chrome_options=set_chrome_opt(1))

    merge_lst = []
    today = str(date.today())
    for thema in themas:
        print(">> We are processing - '%s'." % thema.thema_name)
        url = thema.url
        html = get_page_selenium(url, driver)
        res = get_thema_coinfo(html, thema.thema_name)

        # 테마별 기업리스트 개별 저장
        #save_to_excel(res, col_lab_1, (thema.thema_name).replace('/', ''), today)

        merge_lst = merge_lst + res
        res.clear()

    # 테마별 기업리스트 통합 저장
    save_to_excel(merge_lst, col_lab_1, "★테마별기업통합", today)

    return



'''************************************************
* @Function Name : calc_profit_rate
************************************************'''
def calc_profit_rate(sales, profit):
    try :
        profit_rate = (profit / sales) * 100
        profit_rate = round(profit_rate, 2)
    except:
        profit_rate = ""

    return profit_rate


'''************************************************
* @Function Name : get_thema_coinfo
************************************************'''
def get_thema_coinfo(html, thema_name):
    soup = bs(html, 'html.parser')
    soups = soup.findAll('tr', {'onmouseover': 'mouseOver(this)'})

    AVSL = 3                        #시가총액
    SALES =  4                      #매출액
    B_PROFIT = 5                    #영업이익
    B_PROFIT_RAISE_RATE = 6         #영업이익증가율
    FORIGN_RATE = 7         #외국인비중
    PER = 8                 #PER

    ret_lst = []
    for el in soups:
        info_txt = el.find('p', {'class': 'info_txt'})
        info_txt = info_txt.get_text()
        info_co_name = el.find('div', {'class': 'name_area'})
        info_co_name = info_co_name.get_text()
        info_vals = el.findAll('td', {'class': 'number'})

        #co_info = CoInfo(thema_name, info_co_name, info_txt, info_vals[AVSL], info_vals[B_PROFIT], info_vals[B_PROFIT_RATE], info_vals[FORIGN_RATE], info_vals[PER])
        print(info_co_name)

        try:
            sales_acc = int(info_vals[SALES].get_text().replace(',',''))
            b_profit = int(info_vals[B_PROFIT].get_text().replace(',',''))
            per = float(info_vals[PER].get_text().replace(',',''))

        except:
            sales_acc = 0
            b_profit = 0
            per = 0

        co_info_lst = [thema_name,
                       info_co_name,        #기업명
                       info_txt,            #편입사유
                       int(info_vals[AVSL].get_text().replace(',','')),     #시가총액
                       sales_acc,                                           #매출액
                       info_vals[B_PROFIT].get_text(),                      #영업이익
                       calc_profit_rate(sales_acc, b_profit),       #영업이익률
                       info_vals[B_PROFIT_RAISE_RATE].get_text(),   #영업이익증가율
                       float(info_vals[FORIGN_RATE].get_text()),           #외국인비중
                       per                    #PER
                       ]
        ret_lst.append(co_info_lst)

    return ret_lst


'''************************************************
* @Function Name : save_to_excel
************************************************'''
def save_to_excel(data, col_label, ftitle, today):

    dir_path = """./gen/{0}/""".format(today)
    if not(os.path.isdir(dir_path)):
        os.mkdir(dir_path)

    df = pd.DataFrame(data, columns=col_label)
    fname = """./gen/{0}/{1}_기업리스트.xlsx""".format(today, ftitle)
    df.to_excel(fname, sheet_name='test')

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    res = proc_get_thema()
    proc_get_coinfo(res)
