import asyncio
import math

import requests
import yfinance as yf
from yfinance.exceptions import YFRateLimitError

import schemas
from schemas import Ticker

Graham_Multiplier = 22.5

#-------------------------------------------------------------------------------------
# функция рассчитывает справедливую стоимость акции по формуле Грэма, по заданным параметрам. ВОЗВРАЩАЕТ ЧИСЛО Грэма или None
# The function calculates the fair value of a share using Graham's formula, given the specified parameters. It returns the Graham number or None
#-------------------------------------------------------------------------------------
def graham_value(eps,bvps)->float | None:
    if eps is None or bvps is None or eps <=0 or bvps <=0 :     
        return None
    else :    
        GRAHAM_1949 = math.sqrt(Graham_Multiplier*eps*bvps)
        GRAHAM_NUMBERS = round(GRAHAM_1949,2)
 
    return GRAHAM_NUMBERS

#-------------------------------------------------------------------------------------
# функция собирает параметры по ТИКЕРУ для расчета формулы Грэма (синхронная функция с синхронной библиотекой yfinance)
# The function collects parameters by TICKER to calculate the Graham formula (synchronous function with the synchronous library yfinance)
#-------------------------------------------------------------------------------------
def parameters (ticker_name, session)->list | None :

    list_parameters = []

    stock = yf.Ticker(ticker_name, session=session)
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
        list_parameters.append(None)

    return list_parameters # [longName,currentPrice,currency, eps, bvps]

#-------------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------------
def ticker_full_date_for_DB(ticker_name:str)->Ticker:
# Создаем сессию requests и маскируемся под обычный браузер
# Create a requests session and disguise it as a regular browser
    session = requests.Session()
    session.headers.update({
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    company_parameters = parameters(ticker_name,session)
    if company_parameters is not None :
        eps = company_parameters[3]
        bvps = company_parameters[4]
        gvalue = graham_value(eps,bvps)
        return schemas.Ticker(
        ticker = ticker_name,
        fullname = company_parameters[0],
        price = company_parameters[1],
        currency = company_parameters[2],
        truePrice = gvalue,
        status = status_by_company(company_parameters[1], gvalue)
        )
                     
    else:
        return schemas.Ticker(
        ticker = ticker_name,
        fullname = 'not found',
        price = None,
        currency = None,
        truePrice = None,
        status = 'NO'
        )

def status_by_company(price:float | None, truePrice:float | None)->str:
     if truePrice is None or price is None or price > truePrice: status = 'No' 
     else:status = 'YES'

     return status    
        
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
async def companies_data(list_of_tickers)->dict:
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
            task = tg.create_task(asyncio.to_thread(parameters, i, session))
            task_list.append(task)
            await asyncio.sleep(0.5)

    companies_parameters_list = [task.result() for task in task_list]

# рассчет справедливой стоимость по тикеру 
# calculation of fair value by ticker   
    for i,y in zip(list_of_tickers, companies_parameters_list):
        CompanyData = y 
            
        if CompanyData is not None :
            eps = CompanyData[3]
            bvps = CompanyData[4]
            gvalue = graham_value(eps,bvps)
            CompanyData.append(gvalue)
            all_companies[i] = CompanyData 
        else:
                all_companies[i] = ['not found', None, None, None, None, None]

#    time_finish = time.perf_counter()
#    print(f"total work time {time_finish-time_start} seconds")

    return all_companies

def record_data(cur, all_companies):
    
    for name,param in all_companies.items() :
     
            if param[5] is None or param[1] > param[5] :
                status = 'NO'
            else:
                status = 'YES'
        
            cur.execute('INSERT OR IGNORE INTO Tickers(ticker,fullname,price,currency,truePrice,status) VALUES (?,?,?,?,?,?)',(name,param[0],param[1],param[2],param[5],status))
     
    
        