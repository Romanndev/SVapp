import math
from multiprocessing.util import info
import yfinance as yf
import requests
import sqlite3

list_of_tickers = list()
CompanyData = list()
all_companies = dict()
Graham_Multiplier = 22.5



#-------------------------------------------------------------------------------------
# функция рассчитывает варианты формулы Грэма по заданным параметрам(в год публикации) ВОЗВРАЩАЕТ СЛОВАРЬ
# The function calculates variants of Graham's formula based on the given parameters (in the year of publication) and returns a dictionary.
#-------------------------------------------------------------------------------------
def graham_value(eps,bvps) :
    if eps is None or bvps is None or eps <=0 or bvps <=0 :     
        return None
    else :    
        GRAHAM_1949 = math.sqrt(Graham_Multiplier*eps*bvps)
        GRAHAM_NUMBERS = round(GRAHAM_1949,2)
 
    return GRAHAM_NUMBERS

#-------------------------------------------------------------------------------------
# функция собирает параметры для расчета формул Грэма
# The function collects parameters for calculating Graham's formulas
#-------------------------------------------------------------------------------------
def parameters (ticker_name, session) :

    list_parameters = list()

    stock = yf.Ticker(ticker_name, session=session)
    try:
        info = stock.info
    except :
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
    except :       
     list_parameters.append(None)

    return list_parameters
    


#------------main code-------------------------------------------------------------------------
if __name__ == "__main__":

    # забираем тикеры из файла / We extract tickers from the file   
    try:
     fh = open('list_of_tickers.txt','r')
    except:
        print('Error opening file. File list_of_tickers.txt not found. Please create a file with tickers in the same directory as the script and try again.')
        exit()

    for i in fh :
        ticker_name = i    
        ticker_name = ticker_name.strip().upper()
        ticker_name = ticker_name.replace('/','.')
        ticker_name = ticker_name.replace('-','.')
        ticker_name = ticker_name +'.TO'
        list_of_tickers.append(ticker_name)

    fh.close()

    # Создаем сессию requests и маскируемся под обычный браузер
    # Create a requests session and disguise it as a regular browser
    session = requests.Session()
    session.headers.update({
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    # получить параметры по тикерам, рассчитывать справедливую стоимость
    # Get ticker parameters and calculate fair value

    for i in list_of_tickers :
        CompanyData = parameters (i,session)
        if CompanyData is not None :
            eps = CompanyData[3]
            bvps = CompanyData[4]
            gvalue = graham_value(eps,bvps)
            CompanyData.append(gvalue)
            all_companies[i] = CompanyData 
        else :
            all_companies[i] = ['not found', None, None, None, None, None]

    # сохранить полученные данные и оценку привлекательности к покупке тикеров 
    # save the obtained data and the assessment of the attractiveness of purchasing tickers

    conn = sqlite3.connect('DB_tickers.sqlite')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Tickers (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
            ticker TEXT UNIQUE,
            fullname TEXT UNIQUE,
            price REAL,
            currency TEXT,
            truePrice REAL, 
            status TEXT)                    
                 
    ''')
    cur.execute('''DELETE FROM Tickers''')

    for name,param in all_companies.items() :
 
        if param[5] is None or param[1] > param[5] :
            status = 'NO'
        else:
            status = 'YES'
    
        cur.execute('INSERT OR IGNORE INTO Tickers(id,ticker,fullname,price,currency,truePrice,status) VALUES (?,?,?,?,?,?,?)',(None,name,param[0],param[1],param[2],param[5],status))
 

    conn.commit()
    conn.close()