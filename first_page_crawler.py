import re
import traceback
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from selenium import webdriver
from ticker_name_crawler import ticker

delay = 5

#네이버 금융 기업현황
def Enterprise_Status(code):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    browser_first_p = webdriver.Chrome(options=options)

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser_first_p.get(base_url)

    # frame구조 안으로 들어가기
    browser_first_p.switch_to.frame(browser_first_p.find_element_by_id('coinfo_cp'))
    browser_first_p.find_elements_by_xpath('//*[@id="header-menu"]/div[1]/dl/dt[1]')[0].click()
    browser_first_p.implicitly_wait(delay)

    html0 = browser_first_p.page_source  # 지금 현 상태의 page source불러오기
    html1 = BeautifulSoup(html0, 'html.parser')

    #Dividend Yield 배당수익률 최근 동기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab21"]')[0].click()
    browser_first_p.implicitly_wait(delay)
    htmlDY = browser_first_p.page_source
    htmlDY1 = BeautifulSoup(htmlDY,'html.parser')
    browser_first_p.implicitly_wait(delay)

    htmlfDY = htmlDY1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyDY = htmlfDY.find('tbody')

    try:
        #배당수익률 찾기
        for i in range(0,35):
            if tbodyDY.find_all('th')[i].text == '현금배당수익률':
                cDY = tbodyDY.find_all('th')[i]
                break
            else:
                cDY = None

    except:
        DY =0
        print('error')

    if cDY != None:
        trDY = cDY.parent
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

    # 투자의견
    tbodyAR = htmlART.find('tbody')
    trAR = tbodyAR.find_all('tr')[1]
    tdAR = trAR.find_all('td')[0]
    if trAR.find_all('td')[0].text !='최근3개월 이내에 제시된 의견이 없습니다':
        tdAR = str(tdAR)
        tdAR1 = re.findall("\d+",tdAR)
        tdAR1 = '.'.join(tdAR1)
        AnalystRecom = tdAR1 #투자의견
    else:
        AnalystRecom = 0

    #목표 주가
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

    # EPS growth next year 내년 EPS성장률 최근,미래
    browser_first_p.find_element_by_xpath('//*[@id="cns_Tab21"]').click()
    browser_first_p.implicitly_wait(delay)

    htmlEPSGNb = browser_first_p.page_source  # 지금 현 상태의 page source불러오기
    htmlEPSGNb1 = BeautifulSoup(htmlEPSGNb, 'html.parser')

    htmlEPSGN = htmlEPSGNb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGN = htmlEPSGN.find('tbody')
    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyEPSGN.find_all('th')[i].text == 'EPS(원)':
                cEPSGN = tbodyEPSGN('th')[i]
                break
            else:
                cEPSGN = None

    except:
        EPSGrowthN = 0
        print('error')

    if cEPSGN != None:
        trEPSGN = cEPSGN.parent
        tdEPSGN = trEPSGN.find_all('td')

        EPSGN = []
        EPSGN.append(tdEPSGN[4].text)  # EPS 값 입력
        EPSGN.append(tdEPSGN[5].text)  # EPS 값 입력

        for i in range(len(EPSGN)):  # EPS 값 ,제거
            EPSGN[i] = EPSGN[i].replace(',', '')

        for i in range(len(EPSGN)):  # 공백 제거
            if EPSGN[i] == '':
                EPSGN[i] = '0'

        intEPSGN = list(map(int, EPSGN))
        if intEPSGN[0] != 0:
            divEPSGN = intEPSGN[1] / intEPSGN[0]
            divEPSGN = divEPSGN - 1
            EPSGrowthN = divEPSGN * 100
            EPSGrowthN = round(EPSGrowthN, 2)
        else:
            EPSGrowthN = 0

    # EPS growth past 5 year 지난 5년 EPS성장률 최근,과거
    browser_first_p.find_element_by_xpath('//*[@id="cns_Tab21"]').click()
    browser_first_p.implicitly_wait(delay)

    htmlEPSGP5b = browser_first_p.page_source  # 지금 현 상태의 page source불러오기
    htmlEPSGP5b1 = BeautifulSoup(htmlEPSGP5b, 'html.parser')

    htmlEPSGP5 = htmlEPSGP5b1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGP5 = htmlEPSGP5.find('tbody')

    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyEPSGP5.find_all('th')[i].text == 'EPS(원)':
                cEPSGP5 = tbodyEPSGP5('th')[i]
                break
            else:
                cEPSGP5 = None

    except:
        EPSGrowthP5 = 0
        print('error')

    if cEPSGP5 != None:
        trEPSGP5 = cEPSGP5.parent
        tdEPSGP5 = trEPSGP5.find_all('td')

        EPSGP5 = []
        EPSGP5.append(tdEPSGP5[0].text)  # EPS 값 입력
        EPSGP5.append(tdEPSGP5[4].text)  # EPS 값 입력

        for i in range(len(EPSGP5)):  # EPS 값 ,제거
            EPSGP5[i] = EPSGP5[i].replace(',', '')

        for i in range(len(EPSGP5)):  # 공백 제거
            if EPSGP5[i] == '':
                EPSGP5[i] = '0'

        intEPSGP5 = list(map(int, EPSGP5))
        if intEPSGP5[0] != 0:
            divEPSGP5 = intEPSGP5[1] / intEPSGP5[0]
            divEPSGP5 = divEPSGP5 - 1
            EPSGrowthP5 = divEPSGP5 * 100
            EPSGrowthP5 = round(EPSGrowthP5, 2)
        else:
            EPSGrowthP5 = 0

    # EPS growth next 5 years 향후 5년 EPS성장률 최근,미래
    browser_first_p.find_element_by_xpath('//*[@id="cns_Tab21"]').click()
    browser_first_p.implicitly_wait(delay)

    htmlEPSGN5b = browser_first_p.page_source  # 지금 현 상태의 page source불러오기
    htmlEPSGN5b1 = BeautifulSoup(htmlEPSGN5b, 'html.parser')

    htmlEPSGN5 = htmlEPSGN5b1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGN5 = htmlEPSGN5.find('tbody')

    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyEPSGN5.find_all('th')[i].text == 'EPS(원)':
                cEPSGN5 = tbodyEPSGN5('th')[i]
                break
            else:
                cEPSGN5 = None

    except:
        EPSGrowthN5 = 0
        print('error')

    if cEPSGN5 != None:
        trEPSGN5 = cEPSGN5.parent
        tdEPSGN5 = trEPSGN5.find_all('td')

        EPSGN5 = []
        EPSGN5.append(tdEPSGN5[3].text)  # EPS 값 입력
        EPSGN5.append(tdEPSGN5[7].text)  # EPS 값 입력

        for i in range(len(EPSGN5)):  # EPS 값 ,제거
            EPSGN5[i] = EPSGN5[i].replace(',', '')

        for i in range(len(EPSGN5)):  # 공백 제거
            if EPSGN5[i] == '':
                EPSGN5[i] = '0'

        intEPSGN5 = list(map(int, EPSGN5))

        if intEPSGN5[0] and intEPSGN5[1] != 0:
            divEPSGN5 = intEPSGN5[1] / intEPSGN5[0]
            diEPSGN5 = round(divEPSGN5,2)
            mulEPSGN5 = diEPSGN5 ** (1 / 4)
            mulEPSGN50 = mulEPSGN5 - 1
            muEPSGN5 = mulEPSGN50.real
            EPSGrowthN5 = muEPSGN5 * 100
            EPSGrowthN5 = round(EPSGrowthN5, 2)
        else:
            EPSGrowthN5 = 0

    # Sales growth past 5 years 지난 5년 매출성장률 최근,과거
    browser_first_p.find_element_by_xpath('//*[@id="cns_Tab21"]').click()
    browser_first_p.implicitly_wait(delay)

    htmlSGP5b = browser_first_p.page_source  # 지금 현 상태의 page source불러오기
    htmlSGP5b1 = BeautifulSoup(htmlSGP5b, 'html.parser')

    htmlSGP5 = htmlSGP5b1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodySGP5 = htmlSGP5.find('tbody')

    try:
        # 매출액 찾기
        for i in range(0, 34):
            if tbodySGP5.find_all('th')[i].text == '매출액':
                cSGP5 = tbodySGP5('th')[i]
                break
            else:
                cSGP5 = None

    except:
        SalesGrowthP5 = 0
        print('error')

    if cSGP5 != None:
        trSGP5 = cSGP5.parent
        tdSGP5 = trSGP5.find_all('td')

        SGP5 = []
        SGP5.append(tdSGP5[0].text)
        SGP5.append(tdSGP5[4].text)

        for i in range(len(SGP5)):  #  값 ,제거
            SGP5[i] = SGP5[i].replace(',', '')

        for i in range(len(SGP5)):  # 공백 제거
            if SGP5[i] == '':
                SGP5[i] = '0'

        intSGP5 = list(map(int, SGP5))

        if intSGP5[0] != 0:
            divSGP5 = intSGP5[1] / intSGP5[0]
            mulSGP5 = divSGP5 ** (1 / 4)
            mulSGP50 = mulSGP5 - 1
            SalesGrowthP5 = mulSGP50 * 100
            SalesGrowthP5 = round(SalesGrowthP5, 2)
        else:
            SalesGrowthP5 = 0

    # 재무제표 "분기"
    # P/E 주가수익률 최근 4분기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlPEb = browser_first_p.page_source
    htmlPEb1 = BeautifulSoup(htmlPEb, 'html.parser')
    htmlPE = htmlPEb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyPE = htmlPE.find('tbody')

    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyPE.find_all('th')[i].text == 'EPS(원)':
                cPE = tbodyPE('th')[i]
                break
            else:
                cPE = None

    except:
        PE = 0
        print('error')

    if cPE != None:
        trPE = cPE.parent
        tdPE = trPE.find_all('td')

        EPS0 = []
        for i in range(1, 5):  # EPS 값 입력
            EPS0.append(tdPE[i].text)

        for i in range(len(EPS0)):  # EPS 값 ,제거
            EPS0[i] = EPS0[i].replace(',', '')

        for i in range(len(EPS0)):  # 공백 제거
            if EPS0[i] == '':
                EPS0[i] = '0'

        intEPS = list(map(int, EPS0))
        EPS = sum(intEPS)
        if EPS != 0:
            PE = Price / EPS
            PE = round(PE, 2)
        else:
            PE = 0

    # Forward P/E 예상주가수익률 최근,미래 4분기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlFPEb = browser_first_p.page_source
    htmlFPEb1 = BeautifulSoup(htmlFPEb, 'html.parser')

    htmlFPE = htmlFPEb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyFPE = htmlFPE.find('tbody')

    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyFPE.find_all('th')[i].text == 'EPS(원)':
                cFPE = tbodyFPE('th')[i]
                break
            else:
                cFPE = None

    except:
        FPE = 0
        print('error')

    if cFPE != None:
        trFPE = cFPE.parent
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
        if SumFEPS != 0:
            FPE = int(Price) / SumFEPS
            FPE = round(FPE, 2)
        else:
            FPE = 0

    # EPS growth this year 올해 EPS성장률 최근 4분기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlEPSGTb = browser_first_p.page_source
    htmlEPSGTb1 = BeautifulSoup(htmlEPSGTb, 'html.parser')

    htmlEPSGT = htmlEPSGTb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGT = htmlEPSGT.find('tbody')

    try:
        # EPS 찾기
        for i in range(0, 34):
            if tbodyEPSGT.find_all('th')[i].text == 'EPS(원)':
                cEPSGT = tbodyEPSGT('th')[i]
                break
            else:
                cEPSGT = None

    except:
        EPSGrowthT = 0
        print('error')

    if cEPSGT != None:
        trEPSGT = cEPSGT.parent
        tdEPSGT = trEPSGT.find_all('td')

        EPSGT = []
        EPSGT.append(tdEPSGT[0].text)  # EPS 값 입력
        EPSGT.append(tdEPSGT[4].text)  # EPS 값 입력

        for i in range(len(EPSGT)):  # EPS 값 ,제거
            EPSGT[i] = EPSGT[i].replace(',', '')

        for i in range(len(EPSGT)):  # 공백 제거
            if EPSGT[i] == '':
                EPSGT[i] = '0'

        intEPSGT = list(map(int, EPSGT))

        if intEPSGT[0] != 0:
            divEPSGT = intEPSGT[1] / intEPSGT[0]
            divEPSGT = divEPSGT - 1
            EPSGrowthT = divEPSGT * 100
            EPSGrowthT = round(EPSGrowthT, 2)
        else:
            EPSGrowthT = 0

    # PEG 주가이익성장률 최근 4분기
    if EPSGrowthT != 0:
        PEG = PE / EPSGrowthT
        PEG = round(PEG, 2)
    else:
        PEG = 0

    # P/S 주가매출액비율 최근 4분기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlPSb = browser_first_p.page_source
    htmlPSb1 = BeautifulSoup(htmlPSb, 'html.parser')

    htmlPS = htmlPSb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyPS = htmlPS.find('tbody')


    try:
        # 매출액 찾기
        for i in range(0, 34):
            if tbodyPS.find_all('th')[i].text == '매출액':
                cPS = tbodyPS('th')[i]
                break
            else:
                cPS = None

    except:
        PS = 0
        print('error')

    if cPS != None:
        trPS = cPS.parent
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

        if Sales != 0:
            PS = int(MarketCap) / Sales
            PS = round(PS, 2)
        else:
            PS = 0

    # P/B 주가순자산비율 최근 분기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlPBb = browser_first_p.page_source
    htmlPBb1 = BeautifulSoup(htmlPBb, 'html.parser')

    htmlBP = htmlPBb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyBP = htmlBP.find('tbody')

    try:
        # P/B 찾기
        for i in range(0, 34):
            if tbodyBP.find_all('th')[i].text == 'BPS(원)':
                cBP = tbodyBP('th')[i]
                break
            else:
                cBP = None

    except:
        cBP = 0
        print('error')

    if cBP != None:
        trBP = cBP.parent
        tdBP = trBP.find_all('td')

        BPS0 = 0
        BPS0 = tdBP[4].text  # 값 입력
        BPS0 = BPS0.replace(',', '')

        BPS0 = BPS0.replace(',','')

        if BPS0 == '':
            BPS0 = '0'
        BP = int(BPS0)

        if BP != 0:
            PB = Price / BP  # PBR
            PB = round(PB, 2)
        else:
            BP = 0
            PB = 0

    # P/FC 자유현금흐름비율 최근 4분기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlPFCb = browser_first_p.page_source
    htmlPFCb1 = BeautifulSoup(htmlPFCb, 'html.parser')

    htmlFCF = htmlPFCb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyFCF = htmlFCF.find('tbody')

    try:
        # FCF 찾기
        for i in range(0, 34):
            if tbodyFCF.find_all('th')[i].text == 'FCF':
                cFCF = tbodyFCF('th')[i]
                break
            else:
                cFCF = None

    except:
        PCF = 0
        print('error')

    if cFCF != None:
        trFCF = cFCF.parent
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

        if FCF != 0:
            PFC = Price / FCF
            PFC = round(PFC, 2)
        else:
            PFC = 0

    # ROA 총자산이익률 최근 분기
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlROAb = browser_first_p.page_source
    htmlROAb1 = BeautifulSoup(htmlROAb, 'html.parser')

    htmlROA = htmlROAb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyROA = htmlROA.find('tbody')

    try:
        # ROA 찾기
        for i in range(0, 34):
            if tbodyROA.find_all('th')[i].text == 'ROA(%)':
                cROA = tbodyROA('th')[i]
                break
            else:
                cROA = None

    except:
        ROA = 0
        print('error')

    if cROA != None:
        trROA = cROA.parent
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
    browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab22"]')[0].click()
    browser_first_p.implicitly_wait(delay)

    htmlROEb = browser_first_p.page_source
    htmlROEb1 = BeautifulSoup(htmlROEb, 'html.parser')

    htmlROE = htmlROEb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyROE = htmlROE.find('tbody')

    try:
        # ROE 찾기
        for i in range(0, 34):
            if tbodyROE.find_all('th')[i].text == 'ROE(%)':
                cROE = tbodyROE('th')[i]
                break
            else:
                cROE = None

    except:
        ROE = 0
        print('error')

    if cROE != None:
        trROE = cROE.parent
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


    return DY,Exchange,Industry,Sector,MarketCap,AnalystRecom,\
           TargetPrice,AverageVolume,Price,EPSGrowthN,EPSGrowthP5,\
           EPSGrowthN5,SalesGrowthP5,PE,FPE,EPSGrowthT,PEG,PS,PB,PFC,\
           ROA,ROE


# # try:
# #     for code in ticker:
# #         DY,Exchange,Industry,Sector,MarketCap,AnalystRecom,TargetPrice,AverageVolume,Price,\
# #         EPSGrowthN,EPSGrowthP5,EPSGrowthN5,SalesGrowthP5,PE,FPE,EPSGrowthT,PEG,PS,PB,PFC,\
# #         ROA,ROE = Enterprise_Status(code)
# #
# #         # print(code,DY,Exchange,Industry,Sector,MarketCap,AnalystRecom,TargetPrice,AverageVolume,Price)
# #         # print(EPSGrowthN,EPSGrowthP5,EPSGrowthN5,SalesGrowthP5)
# #         # print(PE,FPE,EPSGrowthT,PEG,PS,PB,PFC,ROA,ROE)
# # except Exception as e:
# #     browser_first_p.quit()
# #     print(traceback.format_exc())
# #     print(e)
#
# code = "047810"
# try:
#     DY, Exchange, Industry, Sector, MarketCap, AnalystRecom, TargetPrice, AverageVolume, Price, \
#     EPSGrowthN, EPSGrowthP5, EPSGrowthN5, SalesGrowthP5, PE, FPE, EPSGrowthT, PEG, PS, PB, PFC, \
#     ROA, ROE = Enterprise_Status(code)
#
#     print(code, DY, Exchange, Industry, Sector, MarketCap, AnalystRecom, TargetPrice, AverageVolume, Price)
#     print(EPSGrowthN, EPSGrowthP5, EPSGrowthN5, SalesGrowthP5)
#     print(PE, FPE, EPSGrowthT, PEG, PS, PB, PFC, ROA, ROE)
#
# except Exception as e:
#     browser_first_p.quit()
#     print(traceback.format_exc())
#     print(e)
#
# browser_first_p.quit()