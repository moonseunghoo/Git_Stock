from pykrx import stock

def All_stock():
    df = stock.get_market_ohlcv_by_ticker('20210217',market='KOSPI')
    list_of_index = [item for item in df.index]
    ticker = sorted(list_of_index) #종목코드 오름차순
    ticker_name = [stock.get_market_ticker_name(i) for i in ticker] # 종목명 오름차순

    return ticker,ticker_name

