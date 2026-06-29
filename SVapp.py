import math
import yfinance as yf
import requests

list_of_tikers = list()
list_parameters = list()
dict_company = dict()


#-------------------------------------------------------------------------------------
# фнкция расчитывает варианты формулы Грэма по заданным параметрам(в год публикации) ВОЗВРАЩАЕТ СЛОВАРЬ
#-------------------------------------------------------------------------------------
def value(eps,bvps) :
          
    GRAHAM_1949 = math.sqrt(22.5*eps*bvps)
    GRAHAM_NUMBERS = round(GRAHAM_1949,2)
 
    return GRAHAM_NUMBERS
#-------------------------------------------------------------------------------------
# функция собирает параметры для расчета формул Грэма
#-------------------------------------------------------------------------------------
def parameters (ticker_name) :

    list_parameters = list()

    # 1. Создаем сессию requests и маскируемся под обычный браузер
    session = requests.Session()
    session.headers.update({
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    stock = yf.Ticker(ticker_name, session=session)
    info = stock.info
    
    #for i in info :
    #    print(i)

    # Достаем параметры для формул Грэма:
    
    financialCurrency = info.get('currency')            # тип валюты
    currentPrice = info.get('currentPrice')             # Текущая рыночная цена
    eps = info.get('trailingEps')                       # EPS (прибыль на акцию за 12 мес.)
    bvps = info.get('bookValue')                        # Балансовая стоимость на акцию
    
    
    list_parameters.append(ticker_name)             # название тикера
    list_parameters.append(info.get('longName'))    # полное название
    list_parameters.append(currentPrice)            # текущий прайс
    list_parameters.append(financialCurrency)       # тип валюты
    list_parameters.append(eps)                     # EPS (прибыль на акцию за 12 мес.)
    list_parameters.append(round(bvps,2))           # Балансовая стоимость на акцию

    return list_parameters

#-------------------------------------------------------------------------------------
# main code
#-------------------------------------------------------------------------------------
#забираем тикеры из файла    
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
    print(i,j)

