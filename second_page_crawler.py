import re
import time
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from selenium import webdriver

delay = 5

#네이버 금융 기업 개요
def Enterprise_Overview(code,browser_second_p):
    try:

        name = code
        base_url = "https://finance.naver.com/item/coinfo.nhn?code=" + name + "&target=finsum_more"

        browser_second_p.get(base_url)

        #frame구조 안으로 들어가기
        browser_second_p.switch_to.frame(browser_second_p.find_element_by_id('coinfo_cp'))

        # 기업공개일
        browser_second_p.find_elements_by_xpath('//*[@class="wrapper-menu"]/dl/dt[2]')[0].click()
        browser_second_p.implicitly_wait(delay)
        htmlCO = browser_second_p.page_source
        htmlCO1 = BeautifulSoup(htmlCO, 'html.parser')

        htmlIPO = htmlCO1.find('table', {'class': 'gHead all-width', 'summary': '기업에 대한 기본적인 정보'
         '(본사주소,홈페이지,대표전화,설립일,대표이사,계열,종업원수,주식수(보통주/우선주),감사인,명의개서,주거래은행)을 제공합니다.'})
        trIPO = htmlIPO.find_all('tr')[3]
        tdIPO = trIPO.find_all('td')[0]

        tdIPO = str(tdIPO)
        tdIPO = re.findall("\d+", tdIPO)
        tdIPO = tdIPO[-3:]
        tdIPO = '/'.join(tdIPO)

        IPODate =tdIPO

        return IPODate
        browser_second_p.close()
    except :
        browser_second_p.close()


# IPODate = []
# for code in ticker:
#     value = Enterprise_Overview(code)
#     print(code,':',value)
#     IPODate.append(value)
#
# print(len(IPODate))

