import time
import traceback
import multiprocessing as multi
from pykrx import stock
from multiprocessing import Process,Queue
from first_page_crawler import Enterprise_Status
from second_page_crawler import Enterprise_Overview
from thrid_page_crawler import Financial_Analysis
from fourth_page_crawler import Investment_Indicators
from Price import Price_a
from ticker_name_crawler import All_stock
from selenium import webdriver

start_time = time.time()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

ticker, ticker_name = All_stock()

def P1(ticker,resultDY,resultExchange,
                resultIndustry,resultSector,resultMarketCap,resultAnalystRecom,
                resultTargetPrice,resultAverageVolume,resultPrice,resultEPSGrowthN,
                resultEPSGrowthP5,resultEPSGrowthN5,resultSalesGrowthP5,resultPE,resultFPE,
                resultEPSGrowthT,resultPEG,resultPS,resultPB,resultPFC,resultROA,resultROE):
    browser_first_p = webdriver.Chrome(options=options)

    DY = []
    Exchange = []
    Industry = []
    Sector = []
    MarketCap = []
    AnalystRecom = []
    TargetPrice = []
    AverageVolume = []
    Price = []
    EPSGrowthN = []
    EPSGrowthP5 = []
    EPSGrowthN5 = []
    SalesGrowthP5 = []
    PE = []
    FPE = []
    EPSGrowthT = []
    PEG = []
    PS = []
    PB = []
    PFC = []
    ROA = []
    ROE = []

    for code in ticker:
        DYv, Exchangev, Industryv, Sectorv, MarketCapv, AnalystRecomv, \
        TargetPricev, AverageVolumev, Pricev, EPSGrowthNv, EPSGrowthP5v, \
        EPSGrowthN5v, SalesGrowthP5v, PEv, FPEv, EPSGrowthTv, PEGv, PSv, PBv, PFCv, \
        ROAv, ROEv = Enterprise_Status(code,browser_first_p)
        print(code,': 1')
        DY.append(DYv)
        Exchange.append(Exchangev)
        Industry.append(Industryv)
        Sector.append(Sectorv)
        MarketCap.append(MarketCapv)
        AnalystRecom.append(AnalystRecomv)
        TargetPrice.append(TargetPricev)
        AverageVolume.append(AverageVolumev)
        Price.append(Pricev)
        EPSGrowthN.append(EPSGrowthNv)
        EPSGrowthP5.append(EPSGrowthP5v)
        EPSGrowthN5.append(EPSGrowthN5v)
        SalesGrowthP5.append(SalesGrowthP5v)
        PE.append(PEv)
        FPE.append(FPEv)
        EPSGrowthT.append(EPSGrowthTv)
        PEG.append(PEGv)
        PS.append(PSv)
        PB.append(PBv)
        PFC.append(PFCv)
        ROA.append(ROAv)
        ROE.append(ROEv)
    browser_first_p.quit()

    resultDY.put(DY)
    resultExchange.put(Exchange)
    resultIndustry.put(Industry)
    resultSector.put(Sector)
    resultMarketCap.put(MarketCap)
    resultAnalystRecom.put(AnalystRecom)
    resultTargetPrice.put(TargetPrice)
    resultAverageVolume.put(AverageVolume)
    resultPrice.put(Price)
    resultEPSGrowthN.put(EPSGrowthN)
    resultEPSGrowthP5.put(EPSGrowthP5)
    resultEPSGrowthN5.put(EPSGrowthN5)
    resultSalesGrowthP5.put(SalesGrowthP5)
    resultPE.put(PE)
    resultFPE.put(FPE)
    resultEPSGrowthT.put(EPSGrowthT)
    resultPEG.put(PEG)
    resultPS.put(PS)
    resultPB.put(PB)
    resultPFC.put(PFC)
    resultROA.put(ROA)
    resultROE.put(ROE)

    return resultDY,resultExchange,resultIndustry,resultSector,\
           resultMarketCap,resultAnalystRecom,resultTargetPrice,\
           resultAverageVolume,resultPrice,resultEPSGrowthN,\
           resultEPSGrowthP5,resultEPSGrowthN5,resultSalesGrowthP5,\
           resultPE,resultFPE,resultEPSGrowthT,resultPEG,resultPS,\
           resultPB,resultPFC,resultROA,resultROE

def P2(ticker,resultIPODate):

    browser_second_p = webdriver.Chrome(options=options)

    IPODate = []
    for code in ticker:
        value = Enterprise_Overview(code,browser_second_p)
        print(code,': 2')
        IPODate.append(value)

    browser_second_p.quit()

    resultIPODate.put(IPODate)
    return resultIPODate

def P3(ticker,resultGM):

    browser_thrid_p = webdriver.Chrome(options=options)

    GM = []
    for code in ticker:
        value = Financial_Analysis(code,browser_thrid_p)
        print(code,': 3')
        GM.append(value)

    browser_thrid_p.quit()

    resultGM.put(GM)
    return resultGM

def P4(ticker,resultPC,resultOM,resultNPM,resultPR,resultCR,resultQR,resultDE):
    browser_price = webdriver.Chrome(options=options)
    browser_fourth_p = webdriver.Chrome(options=options)

    PC = []
    OM =[]
    NPM =[]
    PR =[]
    CR =[]
    QR =[]
    DE = []
    for code in ticker:
        Price = Price_a(code,browser_price)
        PCv,OMv,NPMv,PRv,CRv,QRv,DEv = Investment_Indicators(code,browser_fourth_p,Price)
        print(code,': 4')
        PC.append(PCv)
        OM.append(OMv)
        NPM.append(NPMv)
        PR.append(PRv)
        CR.append(CRv)
        QR.append(QRv)
        DE.append(DEv)

    browser_price.quit()
    browser_fourth_p.quit()

    resultPC.put(PC)
    resultOM.put(OM)
    resultNPM.put(NPM)
    resultPR.put(PR)
    resultCR.put(CR)
    resultQR.put(QR)
    resultDE.put(DE)
    return resultPC,resultOM,resultNPM,resultPR,resultCR,resultQR,resultDE

def main():
    resultDY = Queue()
    resultExchange = Queue()
    resultIndustry = Queue()
    resultSector = Queue()
    resultMarketCap = Queue()
    resultAnalystRecom = Queue()
    resultTargetPrice = Queue()
    resultAverageVolume = Queue()
    resultPrice = Queue()
    resultEPSGrowthN = Queue()
    resultEPSGrowthP5 = Queue()
    resultEPSGrowthN5 = Queue()
    resultSalesGrowthP5 = Queue()
    resultPE = Queue()
    resultFPE = Queue()
    resultDYEPSGrowthT = Queue()
    resultPEG = Queue()
    resultPS = Queue()
    resultPB = Queue()
    resultPFC = Queue()
    resultROA = Queue()
    resultROE = Queue()

    resultIPODate = Queue()

    resultGM = Queue()

    resultPC = Queue()
    resultOM = Queue()
    resultNPM = Queue()
    resultPR = Queue()
    resultCR = Queue()
    resultQR = Queue()
    resultDE = Queue()

    p1 = Process(target=P1, args=(ticker,resultDY,resultExchange,
                resultIndustry,resultSector,resultMarketCap,resultAnalystRecom,
                resultTargetPrice,resultAverageVolume,resultPrice,resultEPSGrowthN,
                resultEPSGrowthP5,resultEPSGrowthN5,resultSalesGrowthP5,resultPE,resultFPE,
                resultDYEPSGrowthT,resultPEG,resultPS,resultPB,resultPFC,resultROA,resultROE))
    p2 = Process(target=P2, args=(ticker, resultIPODate))
    p3 = Process(target=P3, args=(ticker, resultGM))
    p4 = Process(target=P4, args=(ticker, resultPC,resultOM,resultNPM,resultPR,resultCR,resultQR,resultDE))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    valDY = resultDY.get()
    valExchange = resultExchange.get()
    valIndustry = resultIndustry.get()
    valSector = resultSector.get()
    valMarketCap = resultMarketCap.get()
    valAnalystRecom = resultAnalystRecom.get()
    valTargetPrice = resultTargetPrice.get()
    valAverageVolume = resultAverageVolume.get()
    valPrice = resultPrice.get()
    valEPSGrowthN = resultEPSGrowthN.get()
    valEPSGrowthP5 = resultEPSGrowthP5.get()
    valEPSGrowthN5 = resultEPSGrowthN5.get()
    valSalesGrowthP5 = resultSalesGrowthP5.get()
    valPE = resultPE.get()
    valFPE = resultFPE.get()
    valEPSGrowthT = resultDYEPSGrowthT.get()
    valPEG = resultPEG.get()
    valPS = resultPS.get()
    valPB = resultPB.get()
    valPFC = resultPFC.get()
    valROA = resultROA.get()
    valROE = resultROE.get()

    valIPODate = resultIPODate.get()
    valGM = resultGM.get()
    valPC = resultPC.get()
    valOM = resultOM.get()
    valNPM = resultNPM.get()
    valPR = resultPR.get()
    valCR = resultCR.get()
    valQR = resultQR.get()
    valDE = resultDE.get()

    print(valDY)
    print(valExchange)
    print(valIndustry)
    print(valSector)
    print(valMarketCap)
    print(valAnalystRecom)
    print(valTargetPrice)
    print(valAverageVolume)
    print(valPrice)
    print(valEPSGrowthN)
    print(valEPSGrowthP5)
    print(valEPSGrowthN5)
    print(valSalesGrowthP5)
    print(valPE)
    print(valFPE)
    print(valEPSGrowthT)
    print(valPEG)
    print(valPS)
    print(valPB)
    print(valPFC)
    print(valROA)
    print(valROE)

    print(valIPODate)
    print(valGM)
    print(valPC)
    print(valOM)
    print(valNPM)
    print(valPR)
    print(valCR)
    print(valQR)
    print(valDE)

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    return

if __name__ == '__main__':
    main()
    print("MULTI PROCESSING TIME : %s\n" % (time.time() - start_time))





