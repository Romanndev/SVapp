import math
import yfinance as yf
import requests

list_of_tikers = list()
list_parameters = list()
dict_company = dict()


#-------------------------------------------------------------------------------------
# функция рассчитывает варианты формулы Грэма по заданным параметрам(в год публикации) ВОЗВРАЩАЕТ СЛОВАРЬ
# The function calculates variants of Graham's formula based on the given parameters (in the year of publication) and returns a dictionary.
#-------------------------------------------------------------------------------------
def value(eps,bvps) :
          
    GRAHAM_1949 = math.sqrt(22.5*eps*bvps)
    GRAHAM_NUMBERS = round(GRAHAM_1949,2)
 
    return GRAHAM_NUMBERS
#-------------------------------------------------------------------------------------
# функция собирает параметры для расчета формул Грэма
# The function collects parameters for calculating Graham's formulas
#-------------------------------------------------------------------------------------
def parameters (ticker_name) :

    list_parameters = list()

    # Создаем сессию requests и маскируемся под обычный браузер
    # Create a requests session and disguise it as a regular browser
    session = requests.Session()
    session.headers.update({
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    stock = yf.Ticker(ticker_name, session=session)
    info = stock.info
    
    # Достаем параметры для формул Грэма:
    # We get the parameters for Graham's formulas:
    
    currency = info.get('currency')                     # тип валюты / currency type
    currentPrice = info.get('currentPrice')             # Текущая рыночная цена / Current market price
    eps = info.get('trailingEps')                       # EPS (прибыль на акцию за 12 мес.) / EPS (Trailing 12 Month Earnings Per Share)
    bvps = info.get('bookValue')                        # Балансовая стоимость на акцию / Book value per share
    
    
    list_parameters.append(ticker_name)             
    list_parameters.append(info.get('longName'))    
    list_parameters.append(currentPrice)            
    list_parameters.append(currency)                
    list_parameters.append(eps)                     
    list_parameters.append(round(bvps,2))           

    return list_parameters

#-------------------------------------------------------------------------------------
# main code
#-------------------------------------------------------------------------------------
# забираем тикеры из файла / We extract tickers from the file   
fh = open('list_of_tickers.txt','r')

for i in fh :
    ticker_name = i    
    ticker_name = ticker_name.strip().upper()
    ticker_name = ticker_name +'.TO'
    list_of_tikers.append(ticker_name)

fh.close()

for i in list_of_tikers :
    list_parameters = parameters (i)
    dict_company[i] = list_parameters 
    
for i,j in dict_company.items() :
    print(i,j[4],j[5])

# взять параметры и просчитать число грэма

# записать данные из словаря dict_company + число грэма в БД с меткой покупать или нет