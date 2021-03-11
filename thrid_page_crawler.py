import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import traceback
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.

delay = 5

# ticker,ticker_name = All_stock()
# result3 = 0
def Financial_Analysis(code,browser_thrid_p):
    try:
        name = code
        global GM
        base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

        browser_thrid_p.get(base_url)

        # frame구조 안으로 들어가기
        browser_thrid_p.switch_to.frame(browser_thrid_p.find_element_by_id('coinfo_cp'))

        # Gross Margin 매출총이익 최근 4분기
        browser_thrid_p.find_element_by_xpath('//*[@id="header-menu"]/div[1]/dl/dt[3]').click()
        browser_thrid_p.implicitly_wait(delay)
        browser_thrid_p.find_element_by_xpath('//*[@id="frqTyp1"]').click()
        browser_thrid_p.implicitly_wait(delay)
        browser_thrid_p.find_element_by_xpath('//*[@id="hfinGubun"]').click()
        browser_thrid_p.implicitly_wait(delay)
        time.sleep(0.5)

        htmlFA = browser_thrid_p.page_source
        browser_thrid_p.implicitly_wait(delay)
        htmlFA0 = BeautifulSoup(htmlFA, 'html.parser')
        browser_thrid_p.implicitly_wait(delay)
        htmlGM = htmlFA0.find('table', {'class': 'gHead01 all-width data-list'})
        browser_thrid_p.implicitly_wait(delay)

        tbodyGM = htmlGM.find('tbody')

        try:  # 매출총이익 찾기
            cGM = tbodyGM.find('td', {'class': 'txt', 'title': '매출총이익'})
            # pGm = tbodyGM.find_parents('td',{'class':'txt','title':'매출총이익'})

        except:
            GM = 0

        if cGM != None:  # 매출총이익을 찾으면
            trGM = cGM.parent
            tdGM = trGM.find_all('td')

            GM0 = []
            for i in range(2, 6):  # 값 입력
                GM0.append(tdGM[i].text.strip())

            for i in range(len(GM0)):  # 값 ,제거
                GM0[i] = GM0[i].replace(',', '')

            for i in range(len(GM0)):  # 공백 제거
                if GM0[i] == '':
                    GM0[i] = '0'

            strGM = list(map(float, GM0))
            GM = sum(strGM)
            GM = round(GM, 2)

        return GM
        browser_third_p.close()
    except Exception as e :
        browser_third_p.close()
        print(e)
