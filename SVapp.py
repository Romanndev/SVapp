import math
import yfinance as yf
import requests



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

# 1. Создаем сессию requests и маскируемся под обычный браузер
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})


ticker_name = input('Enter ticker name:').strip().upper()
ticker_name = ticker_name +'.TO'
stock = yf.Ticker(ticker_name, session=session)
print(ticker_name)
info = stock.info
print(info.get('longName'))

# Достаем параметры для формул Грэма:
financialCurrency = info.get('financialCurrency')
currentPrice = info.get('currentPrice') # Текущая рыночная цена
eps = info.get('trailingEps')           # EPS (прибыль на акцию за 12 мес.)
bvps = info.get('bookValue')            # Балансовая стоимость на акцию
peg = info.get('pegRatio')              # PEG Ratio (Price/Earnings-to-Growth) расчет по формуле peg= (p/e)/g 
pe = info.get('trailingPE')             # текущий P/E
g = pe/peg                              # Ожидаемый рост прибыли (прогноз 5 лет)
y = 4.38                                # Актуальная ставка на сегодня


print('Curent price=', currentPrice, financialCurrency)
GRAHAM_NUMBERS = value(eps,g,y,bvps)
for i,j in GRAHAM_NUMBERS.items() :
    print(i,j,'CAD')

