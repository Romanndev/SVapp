import asyncio
import time
import math
import random

import requests
import yfinance as yf
from yfinance.exceptions import YFRateLimitError

import schemas

Graham_Multiplier = 22.5

#-------------------------------------------------------------------------------------
# функция рассчитывает справедливую стоимость акции по формуле Грэма, по заданным параметрам. ВОЗВРАЩАЕТ ЧИСЛО Грэма или None
# The function calculates the fair value of a share using Graham's formula, given the specified parameters. It returns the Graham number or None
#-------------------------------------------------------------------------------------
def graham_value(eps,bvps)->float:
    if eps is None or bvps is None or eps <=0 or bvps <=0 :     
        return 0.0
        
    GRAHAM_1949 = math.sqrt(Graham_Multiplier*eps*bvps)
    GRAHAM_NUMBERS = round(GRAHAM_1949,2)
 
    return GRAHAM_NUMBERS

#-------------------------------------------------------------------------------------
# функция собирает параметры по ТИКЕРУ для расчета формулы Грэма (синхронная функция с синхронной библиотекой yfinance)
# The function collects parameters by TICKER to calculate the Graham formula (synchronous function with the synchronous library yfinance)
#-------------------------------------------------------------------------------------
def yfinance_parameters (ticker)->list | None :

    list_parameters = []

    stock = yf.Ticker(ticker) # session=session
    try:
        info = stock.info
    
    except requests.exceptions.RequestException:
         return None
    
    #HTTP Error 404: {"quoteSummary":{"result":null,"error":{"code":"Not Found","description":"Quote not found for symbol: QWERTY.TO"}}}
  
    if info.get('longName') is None:
        return None
        
        # Достаем параметры для формул Грэма:/ We get the parameters for Graham's formulas:
  
    currency = info.get('currency')                     # тип валюты / currency type
    currentPrice = info.get('currentPrice')             # Текущая рыночная цена / Current market price
    eps = info.get('trailingEps')                       # EPS (прибыль на акцию за 12 мес.) / EPS (Trailing 12 Month Earnings Per Share)
    bvps = info.get('bookValue')                        # Балансовая стоимость на акцию / Book value per share
    
                   
    list_parameters.append(info.get('longName'))    
    list_parameters.append(currentPrice)            
    list_parameters.append(currency)                
    list_parameters.append(eps)    
    
    try:                 
        list_parameters.append(round(bvps,2))     
    except (TypeError, ValueError): 
        list_parameters.append(0.0)

    return list_parameters # [longName,currentPrice,currency, eps, bvps]

#-------------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------------
def newticker_date(ticker:str)->schemas.newticker:
# Создаем сессию requests и маскируемся под обычный браузер
# Create a requests session and disguise it as a regular browser
    # session = requests.Session()
    # session.headers.update({
    #        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    #     })
    
    # session = requests.Session()
    # session.headers.update({
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Language': 'en-US,en;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': '1',
    # 'Sec-Fetch-Dest': 'document',
    # 'Sec-Fetch-Mode': 'navigate',
    # 'Sec-Fetch-Site': 'none',
    # 'Sec-Fetch-User': '?1'
    #                        })

    company_parameters = yfinance_parameters(ticker) 
    if company_parameters is not None :
        eps = company_parameters[3]
        bvps = company_parameters[4]
        gvalue = graham_value(eps,bvps)
        
        #[longName,currentPrice,currency, eps, bvps, gvalue]
        return schemas.newticker(
            ticker=ticker,
            fullname=company_parameters[0],
            price=company_parameters[1],
            currency=company_parameters[2],
            eps = company_parameters[3],
            bvps = company_parameters[4],
            truePrice=gvalue,
            status=(schemas.ticker_status.interesting) if company_parameters[1] <= gvalue else (schemas.ticker_status.not_interesting)
        )

    else:
        return schemas.newticker(
            ticker=ticker,
            fullname='no date',
            price=0.0,
            currency='no date',
            eps = 0.0,
            bvps = 0.0,
            truePrice=0.0,
            status= schemas.ticker_status.not_interesting
        )

#-------------------------------------------------------------------------------------
# загрузка списка тикеров из файла
# Loading a list of tickers from a file
#------------------------------------------------------------------------------------- 
def upload_tickers_from_file(file_name)->list: 
    list_of_tickers = []
    try:  
       with open(file_name,'r') as fh:  
    
         for i in fh :
            ticker_name = i    
            ticker_name = ticker_name.strip().upper()
            if not ticker_name:
                 continue
            ticker_name = ticker_name.replace('/','-')
            #ticker_name = ticker_name.replace('-','.')
            ticker_name = ticker_name +'.TO'
            list_of_tickers.append(ticker_name)

    except FileNotFoundError:
           raise FileNotFoundError(f"File '{file_name}' not found in the script directory.")
           
    return list_of_tickers

#-------------------------------------------------------------------------------------
#группируем данные по отдельным компаниям
#grouping data by individual companies  
#-------------------------------------------------------------------------------------
async def companies_data(list_of_tickers)->dict[str,list[float | str]]:
    all_companies = {}

# Создаем сессию requests и маскируемся под обычный браузер
# Create a requests session and disguise it as a regular browser
          
    session = requests.Session()
    session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
         })
    
# получаем параметры по тикерам в асинхноррном режиме
# get ticker parameters in asynchronous mode

#    time_start = time.perf_counter()
    task_list = []
    async with asyncio.TaskGroup() as tg:
        for i in list_of_tickers :
            task = tg.create_task(asyncio.to_thread(yfinance_parameters, i, session))
            task_list.append(task)
            seconds = random.randint(1, 10)
            await asyncio.sleep(seconds)

    companies_parameters = [task.result() for task in task_list]

# рассчет справедливой стоимость по тикеру 
# calculation of fair value by ticker   
    for i,y in zip(list_of_tickers, companies_parameters):
        CompanyData = y 
            
        if CompanyData is not None :
            eps = CompanyData[3]
            bvps = CompanyData[4]
            gvalue = graham_value(eps,bvps)
            CompanyData.append(gvalue)
            all_companies[i] = CompanyData 
        else:
                all_companies[i] = ['no data', 0.0, 'no date', 0.0, 0.0, 0.0] # [longName,currentPrice,currency, eps, bvps, gvalue]

#    time_finish = time.perf_counter()
#    print(f"total work time {time_finish-time_start} seconds")

    return all_companies
  

def test_update(cur):
    #price = []
    cur.execute('''SELECT ticker FROM tsx_stocks''')
    LT = cur.fetchall()
    for i in LT:
      ticker =i[0]
      stock = yf.Ticker(ticker)
      hist = stock.history(period="1d")
      if hist.empty or 'Close' not in hist.columns:
                print(f"Пропущен невалидный тикер: {ticker}")
                continue
      priceP = stock.fast_info['lastPrice'] 
      #price.append(round(priceP))
      time.sleep(10)
      print(ticker,'=', priceP)
    