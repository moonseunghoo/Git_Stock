import requests # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
import pandas as pd # 데이터를 처리하기 위한 가장 기본적인 패키지
import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import urllib.request
import json
import re
import datetime as dt
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime
from selenium.webdriver import Chrome

browser = Chrome()
browser.maximize_window()

def stock_crawler_Annual(code):
    # code = 종목번호
    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser.get(base_url)

    #frame구조 안으로 들어가기
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))

    #재무제표 "연간" 클릭하기
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[3]')[0].click()
    delay = 2
    browser.implicitly_wait(delay)

    html0 = browser.page_source #지금 현 상태의 page source불러오기
    html1 = BeautifulSoup(html0,'html.parser')

    #기업 title불러오기
    title0 = html1.find('head').find('title').text
    title0.split('-')[-1]

    #재무제표 영역 불러오기
    html22 = html1.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})

    #재무제표 영역에서 날짜 불러오기
    thead0 = html22.find('thead')
    tr0 = thead0.find_all('tr')[1]
    th0 = tr0.find_all('th')

    #날자부분만 따로 저장
    date=[]
    for i in range(len(th0)):
        date.append(''.join(re.findall('[0-9/]',th0[i].text)))

    #재무제표 영역에서 columns 및 본문 데이터 수집
    tbody0 = html22.find('tbody') #tbody에 column으로 사용할 데이터와 본문 데이터가 모두 담겨져 있다.
    tr0 = tbody0.find_all('tr')

    #columns 수집
    col = []
    for i in range(len(tr0)):
        if '\xa0' in tr0[i].find('th').text:
            tx = re.sub('\xa0','',tr0[i].find('th').text)
        else:
            tx = tr0[i].find('th').text

        col.append(tx)

    #본문데아터 수집
    td = []
    for i in range(len(tr0)):
        td0 = tr0[i].find_all('td')
        td1 = []
        for j in range(len(td0)):
            if td0[j].text == '':
                td1.append('0')
            else:
                td1.append(td0[j].text)

        td.append(td1)



    return pd.DataFrame(td,columns=date,index=col)

def stock_crawler_Quarter(code):
    # code = 종목번호
    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser.get(base_url)

    #frame구조 안으로 들어가기
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))

    #재무제표 "연간" 클릭하기
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[4]')[0].click()
    delay = 2
    browser.implicitly_wait(delay)

    html0 = browser.page_source #지금 현 상태의 page source불러오기
    html1 = BeautifulSoup(html0,'html.parser')

    #기업 title불러오기
    title0 = html1.find('head').find('title').text
    title0.split('-')[-1]

    #재무제표 영역 불러오기
    html22 = html1.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})

    #재무제표 영역에서 날짜 불러오기
    thead0 = html22.find('thead')
    tr0 = thead0.find_all('tr')[1]
    th0 = tr0.find_all('th')

    #날자부분만 따로 저장
    date=[]
    for i in range(len(th0)):
        date.append(''.join(re.findall('[0-9/]',th0[i].text)))

    #재무제표 영역에서 columns 및 본문 데이터 수집
    tbody0 = html22.find('tbody') #tbody에 column으로 사용할 데이터와 본문 데이터가 모두 담겨져 있다.
    tr0 = tbody0.find_all('tr')

    #columns 수집
    col = []
    for i in range(len(tr0)):
        if '\xa0' in tr0[i].find('th').text:
            tx = re.sub('\xa0','',tr0[i].find('th').text)
        else:
            tx = tr0[i].find('th').text

        col.append(tx)

    #본문데아터 수집
    td = []
    for i in range(len(tr0)):
        td0 = tr0[i].find_all('td')
        td1 = []
        for j in range(len(td0)):
            if td0[j].text == '':
                td1.append('0')
            else:
                td1.append(td0[j].text)

        td.append(td1)



    return pd.DataFrame(td,columns=date,index=col)

code = input('종목코드를 입력하세요.')

stock_Annual_data = stock_crawler_Annual(code)
stock_Quarter_data = stock_crawler_Quarter(code)

writer = pd.ExcelWriter('네이버금융 재무제표 크롤링.xlsx',engine='xlsxwriter')
stock_Annual_data.to_excel(writer,sheet_name='AnnualData')
stock_Quarter_data.to_excel(writer,sheet_name='QuarterData')

writer.save()
