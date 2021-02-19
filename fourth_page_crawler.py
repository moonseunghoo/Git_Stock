import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import traceback
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from selenium import webdriver
from first_page_crawler import Price
from ticker_name_crawler import ticker

start = time.time()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

browser_fourth_p = webdriver.Chrome(options=options)

delay = 5

def Investment_Indicators(code):

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser_fourth_p.get(base_url)

    # frame구조 안으로 들어가기
    browser_fourth_p.switch_to.frame(browser_fourth_p.find_element_by_id('coinfo_cp'))
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_elements_by_xpath('//*[@class="wrapper-menu"]/dl/dt[4]')[0].click()
    browser_fourth_p.implicitly_wait(delay)

    html0 = browser_fourth_p.page_source
    html1 = BeautifulSoup(html0,'html.parser')

    #P/C 주가현금흐름비율 최근 4분기
    browser_fourth_p.find_element_by_xpath('//*[@id="frqTyp1_2"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="hfinGubun2"]').click()
    browser_fourth_p.implicitly_wait(delay)

    htmlPCb = browser_fourth_p.page_source
    htmlPCb1 = BeautifulSoup(htmlPCb, 'html.parser')

    # htmlCPS = htmlPCb1.find('table', {'class': 'gHead01 all-width data-list',
    #                                   'summary': 'IFRS연결 분기 투자분석 정보를 제공합니다.'})

    htmlCPS = htmlPCb1.find_all('table', {'class': 'gHead01 all-width data-list'})[1]
    tbodyCPS = htmlCPS.find('tbody')

    try:  # CPS 찾기
        cCPS = tbodyCPS.find('td', {'class': 'txt', 'title': 'CPS'})

    except:
        CPS = 0

    if cCPS != None:  # CPS을 찾으면
        trCPS = cCPS.parent
        tdCPS = trCPS.find_all('td')

        CPS0 = []
        for i in range(2, 6):
            CPS0.append(tdCPS[i].text)

        for i in range(len(CPS0)):  # 값 ,제거
            CPS0[i] = CPS0[i].replace(',', '')

        for i in range(len(CPS0)):  # 공백 제거
            if CPS0[i] == '':
                CPS0[i] = '0'

        intCPS = list(map(int, CPS0))
        CPS = sum(intCPS)  # CPS

        PC = Price / CPS
        PC = round(PC, 2)

    # Operating Margin 영업이익율 최근 분기
    browser_fourth_p.find_element_by_xpath('//*[@id="val_tab1"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser_fourth_p.implicitly_wait(delay)
    time.sleep(0.5)

    htmlOMb = browser_fourth_p.page_source
    htmlOMb1 = BeautifulSoup(htmlOMb, 'html.parser')

    # htmlOM = htmlOMb1.find('table', {'class': 'gHead01 all-width data-list',
    #                                  'summary': 'IFRS연결 분기 투자분석 정보를 제공합니다.'})

    htmlOM = htmlOMb1.find_all('table', {'class': 'gHead01 all-width data-list'})[0]

    tbodyOM = htmlOM.find('tbody')

    try:  # 영업이익률 찾기
        cOM = tbodyOM.find('td', {'class': 'txt', 'title': '영업이익률'})

    except:
        OM = 0

    if cOM != None:  # 영업이익률을 찾으면
        trOM = cOM.parent
        tdOM = trOM.find_all('td')

        OM0 = []
        OM0.append(tdOM[5].text)

        for i in range(len(OM0)):  # 값 ,제거
            OM0[i] = OM0[i].replace(',', '')

        for i in range(len(OM0)):  # 공백 제거
            if OM0[i] == '':
                OM0[i] = '0'

        strOM = list(map(str, OM0))
        OM = ''.join(strOM)

    # Net Profit Margin 순이익율 최근 분기
    browser_fourth_p.find_element_by_xpath('//*[@id="val_tab1"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser_fourth_p.implicitly_wait(delay)
    time.sleep(0.5)

    htmlNPMb = browser_fourth_p.page_source
    htmlNPMb1 = BeautifulSoup(htmlNPMb, 'html.parser')

    # htmlNPM = htmlNPMb1.find('table', {'class': 'gHead01 all-width data-list',
    #                                   'summary': 'IFRS연결 분기 투자분석 정보를 제공합니다.'})
    htmlNPM = htmlNPMb1.find_all('table', {'class': 'gHead01 all-width data-list'})[0]
    tbodyNPM = htmlNPM.find('tbody')

    try:  # 순이익률 찾기
        cNPM = tbodyNPM.find('td', {'class': 'txt', 'title': '순이익률'})

    except:
        NPM = 0

    if cNPM != None:  # 순이익률을 찾으면
        trNPM = cNPM.parent
        tdNPM = trNPM.find_all('td')

        NPM0 = []
        NPM0.append(tdNPM[5].text)

        for i in range(len(NPM0)):  # 값 ,제거
            NPM0[i] = NPM0[i].replace(',', '')

        for i in range(len(NPM0)):  # 공백 제거
            if NPM0[i] == '':
                NPM0[i] = '0'

        strNPM = list(map(str, NPM0))
        NPM = ''.join(strNPM)

    # Payout Ratio 배당성향 최근 동기
    browser_fourth_p.find_element_by_xpath('//*[@id="frqTyp0_2"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="hfinGubun2"]').click()
    browser_fourth_p.implicitly_wait(delay)
    time.sleep(0.2)

    htmlPRb = browser_fourth_p.page_source
    htmlPRb1 = BeautifulSoup(htmlPRb, 'html.parser')
    # htmlPR = htmlPRb1.find('table', {'class': 'gHead01 all-width data-list',
    #                                  'summary': 'IFRS연결 연간 투자분석 정보를 제공합니다.'})
    htmlPR = htmlPRb1.find_all('table', {'class': 'gHead01 all-width data-list'})[1]

    tbodyPR = htmlPR.find('tbody')

    try:  # 배당성향 찾기
        cPR = tbodyPR.find('td', {'class': 'txt', 'title': '현금배당성향(%)'})

    except:
        PR = 0

    if cPR != None:  # 배당성향을 찾으면
        trPR = cPR.parent
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

    # Current Ratio 유동비율 최근 분기
    browser_fourth_p.find_element_by_xpath('//*[@id="val_tab3"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser_fourth_p.implicitly_wait(delay)
    time.sleep(0.5)

    htmlCRb = browser_fourth_p.page_source
    htmlCRb1 = BeautifulSoup(htmlCRb, 'html.parser')

    htmlCR = htmlCRb1.find_all('table', {'class': 'gHead01 all-width data-list'})[0]

    tbodyCR = htmlCR.find('tbody')

    try:  # 유동비율 찾기
        cCR = tbodyCR.find('td', {'class': 'txt', 'title': '유동비율'})

    except:
        CR = 0

    if cCR != None:  # 유동비율을 찾으면
        trCR = cCR.parent
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

    # Quick Ratio 당좌비율 최근 분기
    browser_fourth_p.find_element_by_xpath('//*[@id="val_tab3"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser_fourth_p.implicitly_wait(delay)
    time.sleep(0.5)

    htmlQRb = browser_fourth_p.page_source
    htmlQRb1 = BeautifulSoup(htmlQRb, 'html.parser')

    htmlQR = htmlQRb1.find_all('table', {'class': 'gHead01 all-width data-list'})[0]
    tbodyQR = htmlQR.find('tbody')

    try:  # 당좌비율 찾기
        cQR = tbodyQR.find('td', {'class': 'txt', 'title': '당좌비율'})

    except:
        QR = 0

    if cQR != None:  # 당좌비율을 찾으면
        trQR = cQR.parent
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

    # Debt/Equity 부채비율 최근 분기
    browser_fourth_p.find_element_by_xpath('//*[@id="val_tab3"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="frqTyp1"]').click()
    browser_fourth_p.implicitly_wait(delay)
    browser_fourth_p.find_element_by_xpath('//*[@id="hfinGubun"]').click()
    browser_fourth_p.implicitly_wait(delay)
    time.sleep(0.5)

    htmlDEb = browser_fourth_p.page_source
    htmlDEb1 = BeautifulSoup(htmlDEb, 'html.parser')

    htmlDE = htmlDEb1.find_all('table', {'class': 'gHead01 all-width data-list'})[0]
    tbodyDE = htmlDE.find('tbody')

    try:  # 부채비율 찾기
        cDE = tbodyDE.find('td', {'class': 'txt', 'title': '부채비율'})

    except:
        DE = 0

    if cDE != None:  # 부채성향을 찾으면
        trDE = cDE.parent
        tdDE = trDE.find_all('td')

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


    return PC,OM,NPM,PR,CR,QR,DE

# try:
#     for code in ticker:
#         PC,OM,NPM,PR,CR,QR,DE = Investment_Indicators(code)
#         print(code)
#         print(PC,OM,NPM,PR,CR,QR,DE)
#
# except Exception as e:
#     browser_fourth_p.quit()
#     print(traceback.format_exc())
#     print(e)
#
# browser_fourth_p.quit()

code = '000020'

try:

    PC,OM,NPM,PR,CR,QR,DE = Investment_Indicators(code)
    print(code)
    print(PC,OM,NPM,PR,CR,QR,DE)

except Exception as e:
    browser_fourth_p.quit()
    print(traceback.format_exc())
    print(e)

browser_fourth_p.quit()
