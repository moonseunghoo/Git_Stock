import time
import traceback
import multiprocessing as multi
from pykrx import stock
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

delay = 5

def Demandedyield():
    browserC = webdriver.Chrome(options=options)

    base_url = 'https://www.kisrating.com/ratingsStatistics/statics_spread.do'
    browserC.get(base_url)
    htmlC0 = browserC.page_source
    htmlC = BeautifulSoup(htmlC0,'html.parser')

    html0 = htmlC.find('div',{'class':'table_ty1'})
    browserC.implicitly_wait(delay)
    trC = html0.find_all('tr')[11]
    tdC = trC.find_all('td')[8]
    tdC = tdC.text
    Demandedyieldv = float(tdC)
    browserC.quit()

    return Demandedyieldv

def Equitycapital(code):
    browserE = webdriver.Chrome(options=options)

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browserE.get(base_url)
    browserE.switch_to.frame(browserE.find_element_by_id('coinfo_cp'))

    browserE.find_element_by_xpath('//*[@id="cns_Tab21"]').click()
    browserE.implicitly_wait(delay)
    htmlE = browserE.page_source
    htmlE0 = BeautifulSoup(htmlE,'html.parser')

    htmlEc = htmlE0.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyE = htmlEc.find('tbody')

    global cE,EC

    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyE.find_all('th')[i].text == '자본총계':
                cE = tbodyE('th')[i+1]
                break
            else:
                cE = None

    except:
        EC = 0
        print('error')

    if cE != None:
        trE = cE.parent
        tdE = trE.find_all('td')

        ECL = tdE[4].text  # EPS 값 입력
        ECL = ECL.replace(',','')
        EC =  int(ECL)
        EC = EC * 100000000

    browserE.quit()
    return EC

def ROE(code):
    browserROE = webdriver.Chrome(options=options)

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browserROE.get(base_url)
    browserROE.switch_to.frame(browserROE.find_element_by_id('coinfo_cp'))

    browserROE.find_element_by_xpath('//*[@id="cns_Tab21"]').click()
    browserROE.implicitly_wait(delay)
    htmlROE = browserROE.page_source
    htmlROE0 = BeautifulSoup(htmlROE, 'html.parser')

    htmlROEc = htmlROE0.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyROE = htmlROEc.find('tbody')

    global cROE, ROE

    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyROE.find_all('th')[i].text == 'ROE(%)':
                cROE = tbodyROE('th')[i]
                break
            else:
                cROE = None

    except:
        ROE = 0
        print('error')

    if cE != None:
        trROE = cROE.parent
        tdROE = trROE.find_all('td')

        if tdROE[5].text != '':
            # ROE0 = tdROE[5].text  # EPS 값 입력
            #
            # ROE0 = ROE0.replace(',','')
            # ROE = float(ROE0)
            p1ROE = float(tdROE[4].text)
            p2ROE = float(tdROE[3].text)
            p3ROE = float(tdROE[2].text)

            ROE = round((p1ROE * 3 + p2ROE * 2 + p3ROE * 1) / 6, 2)
        else:
            p1ROE = float(tdROE[4].text)
            p2ROE = float(tdROE[3].text)
            p3ROE = float(tdROE[2].text)

            ROE = round((p1ROE * 3 + p2ROE * 2 + p3ROE * 1) / 6, 2)

    browserROE.quit()

    return ROE

def shares(code):
    browserSS = webdriver.Chrome(options=options)

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browserSS.get(base_url)
    browserSS.switch_to.frame(browserSS.find_element_by_id('coinfo_cp'))

    htmlSS = browserSS.page_source
    htmlSS0 = BeautifulSoup(htmlSS, 'html.parser')

    htmlSSc = htmlSS0.find('table', {'class': 'gHead', 'summary': '기업의 기본적인 시세정보'
                        '(주가/전일대비/수익률,52주최고/최저,액면가,거래량/거래대금,시가총액,'
                        '유동주식비율,외국인지분율,52주베타,수익률(1M/3M/6M/1Y))를 제공합니다.'})

    tbodySS = htmlSSc.find('tbody')

    trSS = tbodySS.find_all('tr')[6]
    tdSS = trSS.find('td')
    strtd = tdSS.text
    strtd = strtd.strip()
    sptd = strtd.split('/')
    strSS = sptd[0]
    intSS = int(strSS.replace('주','').replace(',',''))

    #자기주식
    htmlMS0 = htmlSS0.find('table',{'class':'gHead01 all-width','summary':'기업의 주요주주의'
                                    ' 보유 주식 수 및 (%) 정보를 제공합니다.'})

    tbodyMS = htmlMS0.find('tbody')

    for i in range(0,11):
        if tbodyMS.find_all('td')[i].text.strip() == '자사주':
            cMS = tbodyMS('td')[i]
            break
        else:
            cMS = None

    if cMS != None:
        trMS = cMS.parent
        tdMS = trMS.find_all('td')
        MS0 = tdMS[1].text.strip()
        strMS = MS0.replace(',','')
        intMS = int(strMS)

    else:
        intMS = 0

    유통주식 = intSS - intMS
    browserSS.quit()
    return 유통주식

code = input('종목코드를 입력하세요 :')

할인률 = Demandedyield()
print(할인률)
자기자본 = Equitycapital(code)
print(자기자본)
ROE = ROE(code)
print(ROE)
초과이익 = round(자기자본 * (ROE - 할인률),2)
print(초과이익)
유통주식 = shares(code)
print(유통주식)
기업가치 = round(자기자본 + (초과이익 / 할인률),2)
print(기업가치)
적정주가 = round(기업가치 / 유통주식,2)
print('적정주가 :',적정주가)