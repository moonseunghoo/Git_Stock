from pykrx import stock

from first_page_crawler import DY,Exchange,Industry,Sector,MarketCap,AnalystRecom,TargetPrice,AverageVolume,Price,\
EPSGrowthN,EPSGrowthP5,EPSGrowthN5,SalesGrowthP5,PE,FPE,EPSGrowthT,PEG,PS,PB,PFC,\
ROA,ROE
from second_page_crawler import IPODate
from thrid_page_crawler import GM
from fourth_page_crawler import PC,OM,NPM,PR,CR,QR,DE
from ticker_name_crawler import ticker,ticker_name

# 상장 기업 종목코드
def All_stock():
    df = stock.get_market_ohlcv_by_ticker('20210214',market='ALL')
    list_of_index = [item for item in df.index]
    ticker = sorted(list_of_index) #종목코드 오름차순
    ticker_name = [stock.get_market_ticker_name(i) for i in ticker] # 종목명 오름차순

    return ticker,ticker_name

code = "000020"




