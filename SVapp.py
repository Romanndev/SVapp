import math
import yfinance as yf
import requests

list_of_tikers = list()
list_parameters = list()
dict_company = dict()


#-------------------------------------------------------------------------------------
# фнкция расчитывает варианты формулы Грэма по заданным параметрам(в год публикации) ВОЗВРАЩАЕТ СЛОВАРЬ
def value(eps,g,y,bvps) :
    GRAHAM_NUMBERS = {}

    GRAHAM_1962 = eps*(8.5 + 2*g)
    GRAHAM_NUMBERS['Graham 1962 formula(with growth forecast):'] = round(GRAHAM_1962,2)
     
    GRAHAM_1974 =((eps*(8.5 + 2*g))*4.4)/y
    GRAHAM_NUMBERS['Graham 1974 formula(with growth forecast):'] = round(GRAHAM_1974,2)
      
    GRAHAM_1949 = math.sqrt(22.5*eps*bvps)
    GRAHAM_NUMBERS['Graham 1949 formula(excluding growth forecast):'] = round(GRAHAM_1949,2)
 
    return GRAHAM_NUMBERS
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
    

    # Достаем параметры для формул Грэма:
    
    financialCurrency = info.get('financialCurrency')   # тип валюты
    currentPrice = info.get('currentPrice')             # Текущая рыночная цена
    eps = info.get('trailingEps')                       # EPS (прибыль на акцию за 12 мес.)
    bvps = info.get('bookValue')                        # Балансовая стоимость на акцию
    peg = info.get('pegRatio')                          # PEG Ratio (Price/Earnings-to-Growth) расчет по формуле peg= (p/e)/g 
    pe = info.get('trailingPE')                         # текущий P/E
    g = pe/peg                                          # Ожидаемый рост прибыли (прогноз 5 лет)
    y = 4.38                                            # Актуальная ставка на сегодня
    
    list_parameters.append(ticker_name)             # название тикера
    list_parameters.append(info.get('longName'))    # полное название
    list_parameters.append(currentPrice)            # текущий прайс
    list_parameters.append(financialCurrency)       # тип валюты
    list_parameters.append(eps)                     # EPS (прибыль на акцию за 12 мес.)
    list_parameters.append(g)                       # Ожидаемый рост прибыли (прогноз 5 лет)
    list_parameters.append(y)                       # Актуальная ставка на сегодня
    list_parameters.append(bvps)                    # Балансовая стоимость на акцию

    return list_parameters

#-------------------------------------------------------------------------------------
# main code
    
fh = open('list_of_tickers.txt','r')

for i in fh :
    ticker_name = i    
    ticker_name = ticker_name.strip().upper()
    ticker_name = ticker_name +'.TO'
    list_of_tikers.append(ticker_name)

fh.close()

for i in list_of_tikers :
    list_parameters = parameters (ticker_name)
    dict_company[ticker_name] = list_parameters 
    
for i,j in dict_company.items() :
    print(i,j)

