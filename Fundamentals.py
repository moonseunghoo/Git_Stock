import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

URL = "https://finance.naver.com/item/coinfo.nhn?code=005930"

samsung_electronic = requests.get(URL)
html = samsung_electronic.text

soup = BeautifulSoup(html, 'html.parser')
print(soup)
