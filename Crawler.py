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

#연간 재무제표
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

#분기별 재무제표
def stock_crawler_Quarter(code):
    # code = 종목번호
    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser.get(base_url)

    #frame구조 안으로 들어가기
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))

    #재무제표 "분기" 클릭하기
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

#기술적 분석
def Descriptive(code):

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser.get(base_url)

    # frame구조 안으로 들어가기
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))

    html0 = browser.page_source  # 지금 현 상태의 page source불러오기
    html1 = BeautifulSoup(html0, 'html.parser')

    # 거래소,산업군,섹터
    htmlEIS = html1.find('td',{'class':'cmp-table-cell td0101'})

    dlEI = htmlEIS.find('dl')
    dtEI = dlEI.find_all('dt',{'class':'line-left'})[1]
    dtS = dlEI.find_all('dt',{'class':'line-left'})[2]

    dtEI = str(dtEI)
    Exchange = dtEI[22:28] #거래소
    Industry = dtEI[29:-5] #산업군

    dtS = str(dtS)
    dtS = dtS[29:-5]
    Sector =  dtS #섹터

    # 평균거래량,시가 총액,가격
    htmlAMP = html1.find('table',{'class':'gHead','summary':'기업의 기본적인 시세정보'
                '(주가/전일대비/수익률,52주최고/최저,액면가,거래량/거래대금,시가총액,유동주식비율,'
                            '외국인지분율,52주베타,수익률(1M/3M/6M/1Y))를 제공합니다.'})

    # 시가총액
    tbodyAM = htmlAMP.find('tbody')
    trM = tbodyAM.find_all('tr')[4]
    tdM = trM.find('td')

    tdM = str(tdM)
    tdM1 = re.findall("\d+",tdM)
    tdM1 = ','.join(tdM1)
    MarketCap = tdM1

    # 평균 거래량
    tbodyAV = htmlAMP.find('tbody')
    trAV = tbodyAV.find_all('tr')[3]
    tdAV = trAV.find('td')

    tdAV = str(tdAV)
    tdAV1 = tdAV[32:-20]
    tdAV1 = tdAV1.split('/')
    tdAV1[1] = ''
    tdAV2 = str(tdAV1[0])
    tdAV2 = re.findall("\d+",tdAV2)
    tdAV2 = ','.join(tdAV2)
    AverageVolume = tdAV2

    # 가격
    tbodyPR = htmlAMP.find('tbody')
    trPR = tbodyPR.find_all('tr')[0]
    tdPR = trPR.find('td')

    tdPR = str(tdPR)
    tdPR = tdPR.split('/')
    tdPR[1:] = ''
    tdPR = str(tdPR)
    tdPR1 = tdPR[58:-3]
    Price = tdPR1.replace(',','')


    # 투자의견,목표 주가
    htmlART = html1.find('table',{'class':'gHead all-width','summary':'투자의견에 대한 '
            '컨센서스의 위치를 그림으로 보여주고, 투자의견값,목표주가,EPS,PER,PBR,추정기관정보를 제공합니다.'})

    tbodyAR = htmlART.find('tbody')
    trAR = tbodyAR.find_all('tr')[1]
    tdAR = trAR.find_all('td')[0]

    tdAR = str(tdAR)
    tdAR1 = re.findall("\d+",tdAR)
    tdAR1 = '.'.join(tdAR1)
    AnalystRecom = tdAR1 #투자의견


    tbodyTP = htmlART.find('tbody')
    trTP = tbodyTP.find_all('tr')[1]
    tdTP = trTP.find_all('td')[1]

    tdTP = str(tdTP)
    tdTP1 = re.findall("\d+", tdTP)
    tdTP1 = '.'.join(tdTP1)
    TargetPrice = tdTP1  # 목표주가

    # 기업공개일
    browser.find_elements_by_xpath('//*[@class="wrapper-menu"]/dl/dt[2]')[0].click()
    delay = 2
    browser.implicitly_wait(delay)
    htmlCO = browser.page_source
    htmlCO1 = BeautifulSoup(htmlCO,'html.parser')

    htmlIPO = htmlCO1.find('table', {'class': 'gHead all-width', 'summary': '기업에 대한 기본적인 정보'
    '(본사주소,홈페이지,대표전화,설립일,대표이사,계열,종업원수,주식수(보통주/우선주),감사인,명의개서,주거래은행)을 제공합니다.'})
    trIPO = htmlIPO.find_all('tr')[3]
    tdIPO = trIPO.find_all('td')[0]

    tdIPO = str(tdIPO)
    tdIPO = re.findall("\d+",tdIPO)
    tdIPO = tdIPO[-3:]
    tdIPO = '/'.join(tdIPO)
    IPODate = tdIPO

    return Exchange,Industry,Sector,MarketCap,AnalystRecom,TargetPrice,AverageVolume,Price,IPODate

#분석 관련 변수
def Fundamental(code,Price):
    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser.get(base_url)

    # frame구조 안으로 들어가기
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))

    html0 = browser.page_source  # 지금 현 상태의 page source불러오기
    html1 = BeautifulSoup(html0, 'html.parser')

    #P/E 주가수익률
    # 재무제표 "분기" 클릭하기
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[4]')[0].click()
    delay = 3
    browser.implicitly_wait(delay)
    htmlQUT = browser.page_source
    htmlQUT1 = BeautifulSoup(htmlQUT,'html.parser')

    htmlPE = htmlQUT1.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})
    tbodyPE = htmlPE.find('tbody')
    trPE = tbodyPE.find_all('tr')[25]
    tdPE = trPE.find_all('td')

    EPS = []
    for i in range(1,5): #EPS 값 입력
        EPS.append(tdPE[i].text)

    for i in range(len(EPS)): #EPS 값 ,제거
        EPS[i] = EPS[i].replace(',','')

    intEPS =  list(map(int,EPS))
    SumEPS = sum(intEPS)
    PE = int(Price)/SumEPS
    PE = round(PE,2)

    #Forward P/E 예상주가수익률
    htmlFPE = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyFPE = htmlFPE.find('tbody')
    trFPE = tbodyFPE.find_all('tr')[25]
    tdFPE = trFPE.find_all('td')

    FEPS = []
    for i in range(4, 8):  # EPS 값 입력
        FEPS.append(tdFPE[i].text)

    for i in range(len(FEPS)):  # EPS 값 ,제거
        FEPS[i] = FEPS[i].replace(',', '')

    intFEPS = list(map(int, FEPS))
    SumFEPS = sum(intFEPS)
    print(SumFEPS)
    print(Price)
    FPE = int(Price) / SumFEPS
    FPE = round(FPE, 2)

    return PE,FPE


code = '005380'
Exchange, Industry, Sector, MarketCap, \
AnalystRecom, TargetPrice, AverageVolume, Price, IPODate = Descriptive(code)

Fundamental = Fundamental(code,Price)
print(Fundamental)