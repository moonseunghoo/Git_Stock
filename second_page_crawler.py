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
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

browser_second_p = webdriver.Chrome(options=options)

delay = 5

#네이버 금융 기업 개요
def Enterprise_Overview(code):
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
    IPODate = tdIPO

    return IPODate

code = "000020"

IPODate = Enterprise_Overview(code)

# print(IPODate)

browser_second_p.quit()