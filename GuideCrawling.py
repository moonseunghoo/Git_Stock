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

a = -0.26 ** (1 / 4)
print(a)
a = a-1
b = a*100

