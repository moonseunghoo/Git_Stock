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
from Crawler import stock_crawler_Annual,stock_crawler_Quarter

code = input('종목코드를 입력하세요.')

stock_Annual_data = stock_crawler_Annual(code)
stock_Quarter_data = stock_crawler_Quarter(code)

writer = pd.ExcelWriter('네이버금융 재무제표 크롤링.xlsx',engine='xlsxwriter')
stock_Annual_data.to_excel(writer,sheet_name='AnnualData')
stock_Quarter_data.to_excel(writer,sheet_name='QuarterData')

writer.save()

