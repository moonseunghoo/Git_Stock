import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import traceback
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.

delay = 5

def Price_a(code,browser_price):

    name = code
    base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

    browser_price.get(base_url)

    # Price 가격
    browser_price.switch_to.frame(browser_price.find_element_by_id('coinfo_cp'))
    browser_price.implicitly_wait(delay)
    browser_price.find_elements_by_xpath('//*[@id="header-menu"]/div[1]/dl/dt[1]')[0].click()
    browser_price.implicitly_wait(delay)

    htmlP = browser_price.page_source  # 지금 현 상태의 page source불러오기
    htmlP1 = BeautifulSoup(htmlP, 'html.parser')

    htmlAMP = htmlP1.find('table', {'class': 'gHead', 'summary': '기업의 기본적인 시세정보'
                   '(주가/전일대비/수익률,52주최고/최저,액면가,거래량/거래대금,시가총액,유동주식비율,'
                   '외국인지분율,52주베타,수익률(1M/3M/6M/1Y))를 제공합니다.'})

    tbodyP = htmlAMP.find('tbody')
    trP = tbodyP.find_all('tr')[0]
    tdP = trP.find('td')

    tdP = str(tdP)
    tdP = tdP.split('/')
    tdP[1:] = ''
    tdP = str(tdP)
    tdP1 = tdP[58:-3]
    Price = tdP1.replace(',', '')
    Price = int(Price)

    return Price