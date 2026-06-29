import math
import yfinance as yf
import requests



# фнкция расчитывает варианты формулы Грэма по заданным параметрам(в год публикации)
def value(eps,g,y,bvps) :
    GRAHAM_1962 = eps*(8.5 + 2*g)
    print('Graham 1962 formula:',GRAHAM_1962)

    GRAHAM_1974 =((eps*(8.5 + 2*g))*4.4)/y
    print('Graham 1974 formula:',GRAHAM_1974)

    GRAHAM_1949 = math.sqrt(22.5*eps*bvps)
    print('Graham 1974 formula:',GRAHAM_1949)

# 1. Создаем сессию requests и маскируемся под обычный браузер
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})


ticker_name = input('Enter ticker name:').strip().upper()
ticker_name = ticker_name +'.TO'
stock = yf.Ticker(ticker_name, session=session)
print(ticker_name)
fast_info = stock.fast_info
for i in fast_info :
    print(i)

print('currency', fast_info['currency'])       # валют тикера
print('lastPrice', fast_info['lastPrice'])     # последний прайс на тикер

#for i in info :
#    print('attribute',i,info.get(i))


# Достаем параметры для формул Грэма:

#current_price = info.get('currentPrice')            # Текущая рыночная цена
#eps = info.get('trailingEps')                       # EPS (прибыль на акцию за 12 мес.)
#bvps = info.get('bookValue')                        # Балансовая стоимость на акцию
#g = info.get('earningsGrowth5Year')                 # Ожидаемый рост прибыли (прогноз 5 лет)
#y = 4.38  # Актуальная ставка на сегодня

#print(current_price,eps,bvps,g,y)