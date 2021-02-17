from selenium import webdriver
import time
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

browser_first_p = webdriver.Chrome(options=options)
delay = 5

# def Financial_Analysis(code):
#     name = code
#     base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"
#
#     browser_thrid_p.get(base_url)
#
#     # frame구조 안으로 들어가기
#     browser_thrid_p.switch_to.frame(browser_thrid_p.find_element_by_id('coinfo_cp'))
#
#     # Gross Margin 매출총이익 최근 4분기
#     browser_thrid_p.find_element_by_xpath('//*[@id="header-menu"]/div[1]/dl/dt[3]').click()
#     browser_thrid_p.implicitly_wait(delay)
#     browser_thrid_p.find_element_by_xpath('//*[@id="frqTyp1"]').click()
#     browser_thrid_p.implicitly_wait(delay)
#     browser_thrid_p.find_element_by_xpath('//*[@id="hfinGubun"]').click()
#     browser_thrid_p.implicitly_wait(delay)
#     time.sleep(0.5)
#
#     htmlFA = browser_thrid_p.page_source
#     htmlFA0 = BeautifulSoup(htmlFA, 'html.parser')
#
#     htmlGM = htmlFA0.find('table', {'class': 'gHead01 all-width data-list'})
#
#     tbodyGM = htmlGM.find('tbody')
#
#     try: #매출총이익 찾기
#         cGM = tbodyGM.find('td',{'class':'txt','title':'매출총이익'})
#         # pGm = tbodyGM.find_parents('td',{'class':'txt','title':'매출총이익'})
#
#     except :
#         GM = 0
#
#     if cGM != None: #매출총이익을 찾으면
#         trGM = cGM.parent
#         tdGM = trGM.find_all('td')
#
#         GM0 = []
#         for i in range(2, 6):  # 값 입력
#             GM0.append(tdGM[i].text)
#
#         for i in range(len(GM0)):  # 값 ,제거
#             GM0[i] = GM0[i].replace(',', '')
#
#         for i in range(len(GM0)):  # 공백 제거
#             if GM0[i] == '':
#                 GM0[i] = '0'
#             else:
#                 break
#
#         strGM = list(map(float, GM0))
#         GM = sum(strGM)
#         GM = round(GM,2)
#
#     return GM
def Enterprise_Status(code):

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
    # browser_first_p.find_elements_by_xpath('//*[@id="cns_Tab21"]')[0].click()
    # browser_first_p.implicitly_wait(delay)
    # htmlDY = browser_first_p.page_source
    # htmlDY1 = BeautifulSoup(htmlDY,'html.parser')
    # browser_first_p.implicitly_wait(delay)
    #
    # htmlfDY = htmlDY1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    # tbodyDY = htmlfDY.find('tbody')
    #
    #
    # try:
    #     #배당수익률 찾기
    #     for i in range(0,35):
    #         if tbodyDY.find_all('th')[i].text == '현금배당수익률':
    #             cDY = tbodyDY.find_all('th')[i]
    #             break
    #         else:
    #             cDY = None
    #
    # except:
    #     DY =0
    #     print('error')
    #
    # if cDY != None:
    #     trDY = cDY.parent
    #     tdDY = trDY.find_all('td')
    #
    #     DY0 = []
    #     DY0.append(tdDY[4].text)
    #
    #     for i in range(len(DY0)):
    #         DY0[i] = DY0[i].replace(',','')
    #
    #     for i in range(len(DY0)):
    #         if DY0[i] == '':
    #             DY0[i] ='0'
    #         else:
    #             break
    #
    #     strDY = list(map(str,DY0))
    #     DY = ''.join(strDY)

    # EPS growth next year 내년 EPS성장률 최근,미래
    browser_first_p.find_element_by_xpath('//*[@id="cns_Tab21"]').click()
    browser_first_p.implicitly_wait(delay)

    htmlEPSGNb = browser_first_p.page_source  # 지금 현 상태의 page source불러오기
    htmlEPSGNb1 = BeautifulSoup(htmlEPSGNb, 'html.parser')

    htmlEPSGN = htmlEPSGNb1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})
    tbodyEPSGN = htmlEPSGN.find('tbody')

    try:
        #EPS 찾기
        for i in range(0,34):
            if tbodyEPSGN.find_all('th')[i].text == 'EPS(원)':
                cEPSGN = tbodyEPSGN('th')[i]
                break
            else:
                cEPSGN = None

    except :
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
        divEPSGN = intEPSGN[1] / intEPSGN[0]
        divEPSGN = divEPSGN - 1
        EPSGrowthN = divEPSGN * 100
        EPSGrowthN = round(EPSGrowthN, 2)



    return EPSGrowthN

code = '000020'
try:
    # GM = Financial_Analysis(code)
    # print(GM)
    EPSGrowthN = Enterprise_Status(code)
    print(EPSGrowthN)
except Exception as e:
    print(e)
    browser_first_p.quit()
browser_first_p.quit()