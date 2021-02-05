# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from tabulate import tabulate
#
# res = requests.get("http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&"
#                    "gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701")
# soup = BeautifulSoup(res.content,'lxml')
# table = soup.find_all('table')
# df = pd.read_html(str(table))
# print(tabulate(df[15],headers='keys',tablefmt='psql'))

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

URL = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&" \
      "gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"

samsung_electronic = requests.get(URL)
html = samsung_electronic.text

soup = BeautifulSoup(html, 'html.parser')
finance_html = soup.select('div.ul_wrap div.um_table')[14]

def annual_data():
    annual_html = soup.select('div.ul_wrap div.um_table')[14]
    th_data = [item.get_text().strip() for item in annual_html.select('thead th')]
    # print(annual_html)
    annual_date = th_data[2:7]
    print(annual_date)
    return annual_date
def quarter_data():
    quarter_html = soup.select('div.ul_wrap div.um_table')[15]
    th_data = [item.get_text().strip() for item in quarter_html.select('thead th')]
    # print(th_data)
    quarter_date = th_data[2:7]
    print(quarter_date)
    return quarter_date
def index_data():
    finance_index = [item.get_text().strip() for item in finance_html.select('th.clf')][1:]
    print(finance_index)

    return finance_index
def finance_data():
    finance_index = [item.get_text().strip() for item in finance_html.select('th.clf')][1:]
    finance_data = [item.get_text().strip() for item in finance_html.select('td')]
    print(finance_data)
    finance_data = np.array(finance_data)
    finance_data.resize(len(finance_index),5)

    return finance_data

# annual_data()
# quarter_data()
index_data()
# finance_data()

# finance_date = annual_data()
# finance = pd.DataFrame(data=finance_data(),index=index_data(),columns=annual_data())
# print(finance)
