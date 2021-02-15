import math

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
from pykrx import stock
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = Chrome()
browser.maximize_window()


# 상장 기업 종목코드
def All_stock():
    df = stock.get_market_ohlcv_by_ticker('20210214',market='ALL')
    list_of_index = [item for item in df.index]
    ticker = sorted(list_of_index) #종목코드 오름차순
    ticker_name = [stock.get_market_ticker_name(i) for i in ticker] # 종목명 오름차순

    return ticker,ticker_name

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

#서술적 분석
def Descriptive(code):

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser.get(base_url)

    # frame구조 안으로 들어가기
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))

    html0 = browser.page_source  # 지금 현 상태의 page source불러오기
    html1 = BeautifulSoup(html0, 'html.parser')

    #Dividend Yield 배당수익률
    browser.find_elements_by_xpath('//*[@id="cns_Tab21"]')[0].click()
    delay = 5
    browser.implicitly_wait(delay)
    htmlDY = browser.page_source
    htmlDY1 = BeautifulSoup(htmlDY,'html.parser')

    htmlfDY = htmlDY1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyDY = htmlfDY.find('tbody')
    trDY = tbodyDY.find_all('tr')[30]
    tdDY = trDY.find_all('td')

    DY0 = []
    DY0.append(tdDY[4].text)

    for i in range(len(DY0)):
        DY0[i] = DY0[i].replace(',','')

    for i in range(len(DY0)):
        if DY0[i] == '':
            DY0[i] ='0'
        else:
            break

    strDY = list(map(str,DY0))
    DY = ''.join(strDY)

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
    MarketCap = tdM1.replace(',','')

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
    Price = int(Price)

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
    tdTP = trTP.find_all('td')

    if len(tdTP) >= 2:
        tdTP = str(tdTP[1])
        tdTP1 = re.findall("\d+", tdTP)
        tdTP1 = '.'.join(tdTP1)
        TargetPrice = tdTP1  # 목표주가
    else:
        TargetPrice = 0

    # 기업공개일
    browser.find_elements_by_xpath('//*[@class="wrapper-menu"]/dl/dt[2]')[0].click()
    delay = 5
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

    return DY,Exchange,Industry,Sector,MarketCap,AnalystRecom,TargetPrice,AverageVolume,Price,IPODate

#분석 관련 변수
def Fundamental(code,Price):
    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser.get(base_url)

    # frame구조 안으로 들어가기
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))

    # 재무제표 "분기" 클릭하기
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[4]')[0].click()
    delay = 5
    browser.implicitly_wait(delay)
    htmlQUT = browser.page_source
    htmlQUT1 = BeautifulSoup(htmlQUT,'html.parser')

    # P/E 주가수익률 최근 4분기
    htmlPE = htmlQUT1.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})
    tbodyPE = htmlPE.find('tbody')
    trPE = tbodyPE.find_all('tr')[25]
    tdPE = trPE.find_all('td')

    EPS0 = []
    for i in range(1,5): #EPS 값 입력
        EPS0.append(tdPE[i].text)

    for i in range(len(EPS0)): #EPS 값 ,제거
        EPS0[i] = EPS0[i].replace(',','')

    for i in range(len(EPS0)):  # 공백 제거
        if EPS0[i] == '':
            EPS0[i] = '0'

    intEPS =  list(map(int,EPS0))
    EPS = sum(intEPS)
    PE = Price/EPS
    PE = round(PE,2)

    #Forward P/E 예상주가수익률 최근,미래 4분기
    htmlFPE = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyFPE = htmlFPE.find('tbody')
    trFPE = tbodyFPE.find_all('tr')[25]
    tdFPE = trFPE.find_all('td')

    FEPS = []
    for i in range(4, 8):  # FEPS 값 입력
        FEPS.append(tdFPE[i].text)

    for i in range(len(FEPS)):  # FEPS 값 ,제거
        FEPS[i] = FEPS[i].replace(',', '')

    for i in range(len(FEPS)):  # FEPS 공백 제거
        if FEPS[i] == '':
            FEPS[i] = '0'

    intFEPS = list(map(int, FEPS))
    SumFEPS = sum(intFEPS)
    FPE = int(Price) / SumFEPS
    FPE = round(FPE, 2)

    #EPS growth this year 올해 EPS성장률 최근 4분기
    htmlEPSGT = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGT = htmlEPSGT.find('tbody')
    trEPSGT = tbodyEPSGT.find_all('tr')[25]
    tdEPSGT = trEPSGT.find_all('td')

    EPSGT = []
    EPSGT.append(tdEPSGT[0].text) #EPS 값 입력
    EPSGT.append(tdEPSGT[4].text) #EPS 값 입력

    for i in range(len(EPSGT)):  # EPS 값 ,제거
        EPSGT[i] = EPSGT[i].replace(',', '')

    for i in range(len(EPSGT)):  # 공백 제거
        if EPSGT[i] == '':
            EPSGT[i] = '0'

    # intEPSG = list(map(int, EPSG))
    # subEPSG = intEPSG[1]-intEPSG[0]
    # divEPSG = subEPSG / intEPSG[0]
    # EPSGrowth = divEPSG * 100
    # EPSGrowth = round(EPSGrowth,2)
    intEPSGT = list(map(int, EPSGT))

    if intEPSGT[0] != 0:
        divEPSGT = intEPSGT[1] / intEPSGT[0]
        divEPSGT = divEPSGT -1
        EPSGrowthT = divEPSGT * 100
        EPSGrowthT = round(EPSGrowthT, 2)
    else:
        EPSGrowthT = 0

    #PEG 주가이익성장률 최근 4분기
    if EPSGrowthT != 0:
        PEG = PE / EPSGrowthT
        PEG = round(PEG,2)
    else:
        PEG = 0

    #P/S 주가매출액비율 최근 4분기
    htmlPS = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyPS = htmlPS.find('tbody')
    trPS = tbodyPS.find_all('tr')[0]
    tdPS = trPS.find_all('td')

    Sale = []
    for i in range(1, 5):  # EPS 값 입력
        Sale.append(tdPS[i].text)

    for i in range(len(Sale)):  # EPS 값 ,제거
        Sale[i] = Sale[i].replace(',', '')

    for i in range(len(Sale)):  # 공백 제거
        if Sale[i] == '':
            Sale[i] = '0'

    intSale = list(map(int, Sale))
    Sales = sum(intSale)

    PS = int(MarketCap) / Sales
    PS = round(PS,2)

    #P/B 주가순자산비율 최근 분기
    htmlBP = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyBP = htmlBP.find('tbody')
    trBP = tbodyBP.find_all('tr')[27]
    tdBP = trBP.find_all('td')

    BPS0 = 0
    BPS0 = tdBP[4].text  # 값 입력
    BPS0 = BPS0.replace(',','')
    BP = int(BPS0)

    PB = Price / BP #PBR
    PB = round(PB,2)

    # P/FC 자유현금흐름비율 최근 4분기
    htmlFCF = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyFCF = htmlFCF.find('tbody')
    trFCF = tbodyFCF.find_all('tr')[17]
    tdFCF = trFCF.find_all('td')

    FCF0 = []
    for i in range(1, 5):  # EPS 값 입력
        FCF0.append(tdFCF[i].text)

    for i in range(len(FCF0)):  # EPS 값 ,제거
        FCF0[i] = FCF0[i].replace(',', '')

    for i in range(len(FCF0)):  # 공백 제거
        if FCF0[i] == '':
            FCF0[i] = '0'

    intFCF = list(map(int, FCF0))
    FCF = sum(intFCF)

    PFC = Price / FCF
    PFC = round(PFC, 2)

    # ROA 총자산이익률 최근 분기
    htmlROA = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyROA = htmlROA.find('tbody')
    trROA = tbodyROA.find_all('tr')[22]
    tdROA = trROA.find_all('td')

    ROA0 = []
    ROA0.append(tdROA[4].text)

    for i in range(len(ROA0)):  # EPS 값 ,제거
        ROA0[i] = ROA0[i].replace(',', '')

    for i in range(len(ROA0)):  # 공백 제거
        if ROA0[i] == '':
            ROA0[i] = '0'

    intROA = list(map(str, ROA0))

    ROA = ''.join(intROA)

    # ROE 자기자본이익률 최근 분기
    htmlROE = htmlQUT1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyROE = htmlROE.find('tbody')
    trROE = tbodyROE.find_all('tr')[21]
    tdROE = trROE.find_all('td')

    ROE0 = []
    ROE0.append(tdROE[4].text)

    for i in range(len(ROE0)):  # EPS 값 ,제거
        ROE0[i] = ROE0[i].replace(',', '')

    for i in range(len(ROE0)):  # 공백 제거
        if ROE0[i] == '':
            ROE0[i] = '0'

    intROE = list(map(str, ROE0))

    ROE = ''.join(intROE)

    # ROI 투자자본수익률

    #P/C 주가현금흐름비율 최근 4분기
    browser.find_elements_by_xpath('//*[@class="wrapper-menu"]/dl/dt[4]')[0].click()
    delay = 5
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="frqTyp1_2"]').click()
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="hfinGubun2"]').click()
    browser.implicitly_wait(delay)

    htmlIIP = browser.page_source
    htmlIIP0 = BeautifulSoup(htmlIIP, 'html.parser')

    htmlCPS = htmlIIP0.find('table',{'class':'gHead01 all-width data-list',
                                    'summary':'IFRS연결 분기 투자분석 정보를 제공합니다.'})
    tbodyCPS = htmlCPS.find('tbody')
    trCPS = tbodyCPS.find_all('tr')[8]
    tdCPS = trCPS.find_all('td')

    CPS0 = []
    for i in range(2,6):
        CPS0.append(tdCPS[i].text)

    for i in range(len(CPS0)): #값 ,제거
        CPS0[i] = CPS0[i].replace(',','')

    for i in range(len(CPS0)):  # 공백 제거
        if CPS0[i] == '':
            CPS0[i] = '0'

    intCPS =  list(map(int,CPS0))
    CPS = sum(intCPS) #CPS

    PC = Price / CPS
    PC = round(PC,2)

    browser.find_element_by_xpath('//*[@id="frqTyp0_2"]').click()
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="hfinGubun2"]').click()
    browser.implicitly_wait(delay)

    # Operating Margin 영업이익율 최근 분기
    browser.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser.implicitly_wait(delay)
    time.sleep(0.5)

    htmlIIP1 = browser.page_source
    htmlIIP2 = BeautifulSoup(htmlIIP1, 'html.parser')

    htmlOM = htmlIIP2.find('table',{'class':'gHead01 all-width data-list',
                                    'summary':'IFRS연결 분기 투자분석 정보를 제공합니다.'})
    tbodyOM = htmlOM.find('tbody')
    trOM = tbodyOM.find_all('tr')[3]
    tdOM = trOM.find_all('td')

    OM0 = []
    OM0.append(tdOM[5].text)

    for i in range(len(OM0)): #값 ,제거
        OM0[i] = OM0[i].replace(',','')

    for i in range(len(OM0)):  # 공백 제거
        if OM0[i] == '':
            OM0[i] = '0'

    strOM =  list(map(str,OM0))
    OM = ''.join(strOM)

    # Net Profit Margin 순이익율 최근 분기
    htmlNPM = htmlIIP2.find('table',{'class':'gHead01 all-width data-list',
                                    'summary':'IFRS연결 분기 투자분석 정보를 제공합니다.'})
    tbodyNPM = htmlNPM.find('tbody')
    trNPM = tbodyNPM.find_all('tr')[6]
    tdNPM = trNPM.find_all('td')

    NPM0 = []
    NPM0.append(tdNPM[5].text)

    for i in range(len(NPM0)): #값 ,제거
        NPM0[i] = NPM0[i].replace(',','')

    for i in range(len(NPM0)):  # 공백 제거
        if NPM0[i] == '':
            NPM0[i] = '0'

    strNPM =  list(map(str,NPM0))
    NPM = ''.join(strNPM)
    time.sleep(0.2)

    # Payout Ratio 배당성향 최근 동기
    htmlPR = htmlIIP2.find('table',{'class':'gHead01 all-width data-list',
                                    'summary':'IFRS연결 연간 투자분석 정보를 제공합니다.'})
    tbodyPR = htmlPR.find('tbody')
    trPR = tbodyPR.find_all('tr')[35]
    tdPR = trPR.find_all('td')

    PR0 = []
    PR0.append(tdPR[5].text)

    for i in range(len(PR0)):  # 값 ,제거
        PR0[i] = PR0[i].replace(',', '')

    for i in range(len(PR0)):  # 공백 제거
        if PR0[i] == '':
            PR0[i] = '0'

    strPR = list(map(str, PR0))
    PR = ''.join(strPR)

    #Current Ratio 유동비율 최근 분기
    browser.find_element_by_xpath('//*[@id="val_td3"]').click()
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser.implicitly_wait(delay)
    time.sleep(0.5)

    htmlIIS = browser.page_source
    htmlIIS0 = BeautifulSoup(htmlIIS, 'html.parser')
    htmlCR = htmlIIS0.find_all('table',{'class':'gHead01 all-width data-list'})[0]

    tbodyCR = htmlCR.find('tbody')
    trCR = tbodyCR.find_all('tr')[12]
    tdCR = trCR.find_all('td')

    CR0 = []
    CR0.append(tdCR[5].text)

    for i in range(len(CR0)):  # 값 ,제거
        CR0[i] = CR0[i].replace(',', '')

    for i in range(len(CR0)):  # 공백 제거
        if CR0[i] == '':
            CR0[i] = '0'
        else:
            break

    intCR = list(map(str, CR0))
    CR = ''.join(intCR)

    #Quick Ratio 당좌비율 최근 분기
    htmlQR = htmlIIS0.find_all('table', {'class': 'gHead01 all-width data-list'})[0]
    tbodyQR = htmlQR.find('tbody')
    trQR = tbodyQR.find_all('tr')[15]
    tdQR = trQR.find_all('td')

    QR0 = []
    QR0.append(tdQR[5].text)

    for i in range(len(QR0)):  # 값 ,제거
        QR0[i] = QR0[i].replace(',', '')

    for i in range(len(QR0)):  # 공백 제거
        if QR0[i] == '':
            QR0[i] = '0'
        else:
            break

    intQR = list(map(str, QR0))
    QR = ''.join(intQR)

    #Debt/Equity 부채비율 최근 분기
    htmlDE = htmlIIS0.find_all('table', {'class': 'gHead01 all-width data-list'})[0]
    tbodyDE = htmlDE.find('tbody')
    trDE = tbodyDE.find_all('tr')[0]
    tdDE = trDE.find_all('td')

    DE0 = []
    DE0.append(tdDE[5].text)

    for i in range(len(DE0)):  # 값 ,제거
        DE0[i] = DE0[i].replace(',', '')

    for i in range(len(DE0)):  # 공백 제거
        if DE0[i] == '':
            DE0[i] = '0'
        else:
            break

    intDE = list(map(str, DE0))
    DE = ''.join(intDE)

    #Gross Margin 매출총이익 최근 4분기
    browser.find_element_by_xpath('//*[@id="header-menu"]/div[1]/dl/dt[3]').click()
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser.implicitly_wait(delay)
    time.sleep(0.5)

    htmlFA = browser.page_source
    htmlFA0 = BeautifulSoup(htmlFA, 'html.parser')
    htmlGM = htmlFA0.find('table', {'class': 'gHead01 all-width data-list'})

    tbodyGM = htmlGM.find('tbody')
    trGM = tbodyGM.find_all('tr')[25]
    tdGM = trGM.find_all('td')

    GM0 = []
    for i in range(2, 6):  # EPS 값 입력
        GM0.append(tdGM[i].text)

    for i in range(len(GM0)):  # 값 ,제거
        GM0[i] = GM0[i].replace(',', '')

    for i in range(len(GM0)):  # 공백 제거
        if GM0[i] == '':
            GM0[i] = '0'
        else:
            break

    strGM = list(map(float, GM0))
    GM = sum(strGM)

    # 재무제표 "연간" 클릭하기
    browser.find_elements_by_xpath('//*[@id="header-menu"]/div[1]/dl/dt[1]')[0].click()
    browser.implicitly_wait(delay)
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[3]')[0].click()
    browser.implicitly_wait(delay)
    htmlANU = browser.page_source  # 지금 현 상태의 page source불러오기
    htmlANU1 = BeautifulSoup(htmlANU, 'html.parser')

    # EPS growth next year 내년 EPS성장률 최근,미래
    htmlEPSGN = htmlANU1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGN = htmlEPSGN.find('tbody')
    trEPSGN = tbodyEPSGN.find_all('tr')[25]
    tdEPSGN = trEPSGN.find_all('td')

    EPSGN = []
    EPSGN.append(tdEPSGN[4].text)  # EPS 값 입력
    EPSGN.append(tdEPSGN[5].text)  # EPS 값 입력

    for i in range(len(EPSGN)):  # EPS 값 ,제거
        EPSGN[i] = EPSGN[i].replace(',', '')

    # intEPSG = list(map(int, EPSG))
    # subEPSG = intEPSG[1]-intEPSG[0]
    # divEPSG = subEPSG / intEPSG[0]
    # EPSGrowth = divEPSG * 100
    # EPSGrowth = round(EPSGrowth,2)
    for i in range(len(EPSGN)):  # 공백 제거
        if EPSGN[i] == '':
            EPSGN[i] = '0'

    intEPSGN = list(map(int, EPSGN))
    divEPSGN = intEPSGN[1] / intEPSGN[0]
    divEPSGN = divEPSGN - 1
    EPSGrowthN = divEPSGN * 100
    EPSGrowthN = round(EPSGrowthN, 2)

    # EPS growth past 5 year 지난 5년 EPS성장률 최근,과거
    htmlEPSGP5 = htmlANU1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGP5 = htmlEPSGP5.find('tbody')
    trEPSGP5 = tbodyEPSGP5.find_all('tr')[25]
    tdEPSGP5 = trEPSGP5.find_all('td')

    EPSGP5 = []
    EPSGP5.append(tdEPSGP5[0].text)
    EPSGP5.append(tdEPSGP5[4].text)

    for i in range(len(EPSGP5)):  # EPS 값 ,제거
        EPSGP5[i] = EPSGP5[i].replace(',', '')

    for i in range(len(EPSGP5)):  # 공백 제거
        if EPSGP5[i] == '':
            EPSGP5[i] = '0'

    # intEPSG = list(map(int, EPSG))
    # subEPSG = intEPSG[1]-intEPSG[0]
    # divEPSG = subEPSG / intEPSG[0]
    # EPSGrowth = divEPSG * 100
    # EPSGrowth = round(EPSGrowth,2)
    intEPSGP5 = list(map(int, EPSGP5))

    if intEPSGP5[0] !=0:
        divEPSGP5 = intEPSGP5[1] / intEPSGP5[0]
        mulEPSGP5 = divEPSGP5**(1/4)
        mulEPSGP50 = mulEPSGP5 - 1
        EPSGrowthP5 = mulEPSGP50 * 100
        EPSGrowthP5 = round(EPSGrowthP5, 2)
    else:
        EPSGrowthP5 = 0

    # EPS growth next 5 years 향후 5년 EPS성장률 최근,미래
    htmlEPSGN5 = htmlANU1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGN5 = htmlEPSGN5.find('tbody')
    trEPSGN5 = tbodyEPSGN5.find_all('tr')[25]
    tdEPSGN5 = trEPSGN5.find_all('td')

    EPSGN5 = []
    EPSGN5.append(tdEPSGN5[3].text)
    EPSGN5.append(tdEPSGN5[7].text)

    for i in range(len(EPSGN5)):  # EPS 값 ,제거
        EPSGN5[i] = EPSGN5[i].replace(',', '')

    for i in range(len(EPSGN5)):  # 공백 제거
        if EPSGN5[i] == '':
            EPSGN5[i] = '0'

    # intEPSG = list(map(int, EPSG))
    # subEPSG = intEPSG[1]-intEPSG[0]
    # divEPSG = subEPSG / intEPSG[0]
    # EPSGrowth = divEPSG * 100
    # EPSGrowth = round(EPSGrowth,2)
    intEPSGN5 = list(map(int, EPSGN5))

    if intEPSGN5[0] != 0:
        divEPSGN5 = intEPSGN5[1] / intEPSGN5[0]
        mulEPSGN5 = divEPSGN5 ** (1 / 4)
        mulEPSGN50 = mulEPSGN5 - 1
        EPSGrowthN5 = mulEPSGN50 * 100
        EPSGrowthN5 = round(EPSGrowthN5, 2)
    else:
        EPSGrowthN5 = 0

    # Sales growth past 5 years 지난 5년 매출성장률 최근,과거
    htmlSGP5 = htmlANU1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodySGP5 = htmlSGP5.find('tbody')
    trSGP5 = tbodySGP5.find_all('tr')[0]
    tdSGP5 = trSGP5.find_all('td')

    SGP5 = []
    SGP5.append(tdSGP5[0].text)
    SGP5.append(tdSGP5[4].text)

    for i in range(len(SGP5)):  # EPS 값 ,제거
        SGP5[i] = SGP5[i].replace(',', '')

    for i in range(len(SGP5)):  # 공백 제거
        if SGP5[i] == '':
            SGP5[i] = '0'

    # intEPSG = list(map(int, EPSG))
    # subEPSG = intEPSG[1]-intEPSG[0]
    # divEPSG = subEPSG / intEPSG[0]
    # EPSGrowth = divEPSG * 100
    # EPSGrowth = round(EPSGrowth,2)
    intSGP5 = list(map(int, SGP5))

    if intSGP5[0] != 0:
        divSGP5 = intSGP5[1] / intSGP5[0]
        mulSGP5 = divSGP5 ** (1 / 4)
        mulSGP50 = mulSGP5 - 1
        SalesGrowthP5 = mulSGP50 * 100
        SalesGrowthP5 = round(SalesGrowthP5, 2)
    else:
        SalesGrowthP5 = 0




    return PE, FPE, EPSGrowthT, PEG, PS, PB, CPS, PC,\
           FCF, PFC, EPSGrowthN, EPSGrowthP5, EPSGrowthN5,\
           SalesGrowthP5, ROA, ROE, CR, QR, DE, GM, OM, NPM, PR

#기술적 분석
def Technical(code):
    return


#출력 함수
def PrintA(DY, Exchange, Industry, Sector, MarketCap, \
AnalystRecom, TargetPrice, AverageVolume, Price,
IPODate,PE,FPE, EPSGrowthT, PEG, PS, PB, CPS, PC, FCF,\
PFC, EPSGrowthN, EPSGrowthP5, EPSGrowthN5, SalesGrowthP5, ROA,\
ROE, CR, QR, DE, GM, OM, NPM, PR):

    print('----Descriptive----')
    print('Exchange : ',Exchange)
    print('Indusrty : ',Industry)
    print('Sector : ',Sector)
    print('MarketCap : ',MarketCap)
    print('AnalystRecom : ',AnalystRecom)
    print('TargetPrice : ',TargetPrice)
    print('AverageVolume : ',AverageVolume)
    print('Price : ',Price)
    print('Dividend Yield : ',DY)
    print('IPODate : ',IPODate)
    print('----Fundamental----')
    print('P/E ratio : ', PE)
    print('Forward P/E ratio : ', FPE)
    print('EPS Growth ratio this year : ', EPSGrowthT)
    print('EPS Growth ratio next year : ', EPSGrowthN)
    print('EPS Growth ratio past 5 year : ', EPSGrowthP5)
    print('EPS Growth ratio next 5 year : ', EPSGrowthN5)
    print('Sales Growth ratio past 5 year : ', SalesGrowthP5)
    print('PEG Growth ratio : ', PEG)
    print('P/S ratio : ', PS)
    print('P/B ratio : ', PB)
    print('P/C ratio : ', PC)
    print('P/FC ratio : ', PFC)
    print('ROA ratio : ', ROA)
    print('ROE ratio : ', ROE)
    print('Current ratio : ', CR)
    print('Quick ratio : ', QR)
    print('Debt/Equity : ', DE)
    print('Gross Margin : ', GM)
    print('Operating Margin : ', OM)
    print('Net Profit Margin : ', NPM)
    print('Payout Ratio : ', PR)

    return



ticker, ticker_name = All_stock()

# for code in ticker:
#     DY, Exchange, Industry, Sector, MarketCap, \
#     AnalystRecom, TargetPrice, AverageVolume, Price, IPODate = Descriptive(code)
#
#     PE, FPE, EPSGrowthT, PEG, PS, PB, CPS, PC, FCF,\
#     PFC, EPSGrowthN, EPSGrowthP5, EPSGrowthN5, SalesGrowthP5, ROA,\
#     ROE, CR, QR, DE, GM, OM, NPM, PR = Fundamental(code,Price)
#
#     PrintA(DY, Exchange, Industry, Sector, MarketCap, \
#     AnalystRecom, TargetPrice, AverageVolume, Price,
#     IPODate,PE, FPE, EPSGrowthT, PEG, PS, PB, CPS, PC, FCF,\
#     PFC, EPSGrowthN, EPSGrowthP5, EPSGrowthN5, SalesGrowthP5, ROA,\
#     ROE, CR, QR, DE, GM, OM, NPM, PR)


code = "000020"

DY, Exchange, Industry, Sector, MarketCap, \
AnalystRecom, TargetPrice, AverageVolume, Price, IPODate = Descriptive(code)

PE, FPE, EPSGrowthT, PEG, PS, PB, CPS, PC, FCF,\
PFC, EPSGrowthN, EPSGrowthP5, EPSGrowthN5, SalesGrowthP5, ROA,\
ROE, CR, QR, DE, GM, OM, NPM, PR = Fundamental(code,Price)

PrintA(DY, Exchange, Industry, Sector, MarketCap, \
AnalystRecom, TargetPrice, AverageVolume, Price,
IPODate,PE, FPE, EPSGrowthT, PEG, PS, PB, CPS, PC, FCF,\
PFC, EPSGrowthN, EPSGrowthP5, EPSGrowthN5, SalesGrowthP5, ROA,\
ROE, CR, QR, DE, GM, OM, NPM, PR)


