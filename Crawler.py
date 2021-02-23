import time
import traceback
import multiprocessing as multi
from pykrx import stock
from multiprocessing import Process,Queue
from first_page_crawler import Enterprise_Status
from second_page_crawler import Enterprise_Overview
from thrid_page_crawler import Financial_Analysis
from fourth_page_crawler import Investment_Indicators
from ticker_name_crawler import All_stock

start_time = time.time()

if __name__ == '__main__':
    code = '005380'

    try:
        result1 = Queue()
        result2 = Queue()
        result3 = Queue()
        result4 = Queue()
        th1 = Process(target=Enterprise_Status, args=(1, code, result1))
        th2 = Process(target=Enterprise_Overview, args=(2, code, result2))
        th3 = Process(target=Financial_Analysis, args=(3, code, result3))
        th4 = Process(target=Investment_Indicators, args=(4,code,result4))

        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th1.join()
        th2.join()
        th3.join()
        th4.join()

        DY = result1.get()
        Exchange = result1.get()
        Industry = result1.get()
        Sector = result1.get()
        MarketCap = result1.get()
        AverageVolume = result1.get()
        Price = result1.get()
        AnalystRecom = result1.get()
        TargetPrice = result1.get()
        EPSGrowthN = result1.get()
        EPSGrowthP5 = result1.get()
        EPSGrowthN5 = result1.get()
        SalesGrowthP5 = result1.get()
        PE = result1.get()
        FPE = result1.get()
        EPSGrowthT = result1.get()
        PEG = result1.get()
        PS = result1.get()
        PB = result1.get()
        PFC = result1.get()
        ROA = result1.get()
        ROE = result1.get()
        IPODate = result2.get()
        GM = result3.get()
        PC = result4.get()
        OM = result4.get()
        NPM = result4.get()
        PR = result4.get()
        CR = result4.get()
        QR = result4.get()
        DE = result4.get()

        print(Exchange,Industry,Sector,MarketCap,Price)
        print(PE,FPE,PEG,PS,PB,PFC,ROA,ROE,DY)
        print(AverageVolume,AnalystRecom,TargetPrice)
        print(EPSGrowthT,EPSGrowthN,EPSGrowthP5,EPSGrowthN5,SalesGrowthP5)
        print(IPODate)
        print(GM)
        print(PC,OM,NPM,PR,CR,QR,DE)

    except Exception as e:
        print(traceback.format_exc())
        print(e)

print('--- %s seconds ---' % (time.time() - start_time))





