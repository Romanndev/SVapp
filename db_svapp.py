import datetime
import os

#import sqlite3
from contextlib import contextmanager
from typing import Any
from zoneinfo import ZoneInfo

import psycopg2

import schemas
import stocks_valuation as sv
from schemas import ticker_status


@contextmanager
def get_db_connection():
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        #conn = sqlite3.connect('tickers.db')
        cur = conn.cursor()
        create_table(cur)
        try:
            yield conn
            conn.commit()
            conn.close()
        finally:
            conn.close()
              
# создание таблицы
def create_table(cur):
    try :
        cur.execute("""CREATE TABLE IF NOT EXISTS tsx_stocks (
                id INT8 NOT NULL DEFAULT unique_rowid(),
                ticker STRING UNIQUE,
                fullname STRING,
                price FLOAT4,
                currency STRING,
                eps FLOAT4,
                bvps FLOAT4,
                truePrice FLOAT4,
                status STRING,
                update_date DATE DEFAULT current_timestamp():::DATE,
                CONSTRAINT tsx_stocks_pkey PRIMARY KEY (id ASC)
                )"""
                    ) # [longName,currentPrice,currency, eps, bvps, gvalue]
           
    except psycopg2.Error as e:
        raise psycopg2.OperationalError(f"Error, table creation: '{e}'")

# удаление таблицы
def drop_table(cur):
    cur.execute('''DROP TABLE IF EXISTS tsx_stocks CASCADE''')

# интересные тикеры для покупки
def ineteresting_tickers(cur)->list[dict[str,Any]]:
    result = []
    cur.execute('''SELECT * FROM tsx_stocks WHERE status=%s''',(ticker_status.interesting.value,))
    rows = cur.fetchall()
    
    for row in rows:
        result.append({
                    'ticker': row[1],
                    'fullname': row[2],
                    'price': row[3],
                    'currency': row[4],
                    'truePrice': row[7],
                    'status': row[8],
                    'id': row[0],
                    'update_date': row[9]
                    
                    })
    
    return  result

# не интересные тикеры для покупки
def not_ineteresting_tickers(cur)->list[dict[str,Any]]:
    result = []
    cur.execute('''SELECT * FROM tsx_stocks WHERE status=%s''',(ticker_status.not_interesting.value,))
    rows = cur.fetchall()
    
    for row in rows:
        result.append({
                    'ticker': row[1],
                    'fullname': row[2],
                    'price': row[3],
                    'currency': row[4],
                    'truePrice': row[7],
                    'status': row[8],
                    'id': row[0],
                    'update_date': row[9]
                    
                    })
    
    return  result

def check_ticker_name(ticker):
     ticker = ticker.upper()

     if ticker.startswith('-') : ticker = ticker.removeprefix('-')
     if ticker.startswith('.') : ticker = ticker.removeprefix('.')
     #if ticker.startswith('/') : ticker = ticker.removeprefix('/')
     
     if ticker.find('/') != -1: ticker = ticker.replace('/','-')
    
     if ticker.endswith('-'): ticker = ticker[:-1].replace('-','.TO')
     if ticker.endswith('.'): ticker = ticker[:-1].replace('.','.TO')
     if ticker.endswith('/'): ticker = ticker[:-1].replace('.','.TO')
     
     if ticker.find('.TO') == -1: ticker = ticker + '.TO'

     return ticker   

# информация по тикеру
def ticker_info(cur,ticker:str)->dict[str,Any] | None: 
    ticker = check_ticker_name(ticker)  
    cur.execute('''SELECT * FROM tsx_stocks WHERE ticker=%s''',(ticker,))
    row =cur.fetchone()
    
    if row is None: return None
    
    return {
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'truePrice': row[7], 
                'status': row[8],
                'id': row[0],
                'update_date': row[9]
                }

# добавление нового тикера в БД
def save_new_ticker(cur, newticker_date: schemas.newticker)->dict[str, Any]:
    ticker = newticker_date.ticker
    fullname = newticker_date.fullname
    price = newticker_date.price
    currency = newticker_date.currency
    eps = newticker_date.eps
    bvps = newticker_date.bvps
    trueprice = newticker_date.truePrice
    status = newticker_date.status.value

    cur.execute('''INSERT INTO tsx_stocks(ticker, fullname, price, currency,eps,bvps,truePrice, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (ticker) DO NOTHING''', (ticker, fullname, price, currency,eps,bvps,trueprice, status))
    cur.execute('''SELECT * FROM tsx_stocks WHERE ticker=%s''',(ticker,))
    row = cur.fetchone() 
    
    return {
                'id': row[0],
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'truePrice': row[7], 
                'status': row[8],
                'update_date': row[9]
                }
 
#обновление данных по всем тикерам в БД
async def update_all(cur):
    tickerslist = []
    company_data = {}
    current_date = datetime.datetime.now(ZoneInfo("America/Edmonton")).date()
    tickerslist = tickersupdate(cur,current_date)
    if not tickerslist: 
        return {'status':'Tickers are updated'}

    company_data = await sv.companies_data(tickerslist)
    for ticker, param in company_data.items():  
         if  param[5] == 0 or param[1] > param[5]:
            cur.execute('''UPDATE tsx_stocks SET price=%s,truePrice=%s,status=%s,update_date=%s WHERE ticker=%s''',(param[1],param[5],ticker_status.not_interesting.value,current_date,ticker))

         elif param[1]< param[5]:
            cur.execute('''UPDATE tsx_stocks SET price=%s,truePrice=%s,status=%s,update_date=%s WHERE ticker=%s''',(param[1],param[5],ticker_status.interesting.value,current_date,ticker))

    return {'status':'Tickers are updated...'}

def tickersupdate(cur,current_date)->list[str]:
    tickerslist = []
    cur.execute('''SELECT ticker FROM tsx_stocks WHERE update_date < %s''',(current_date,))
    tickerslist = cur.fetchone() #cur.fetchall()
    if tickerslist is None or len(tickerslist) == 0: 
        return [] # empty list if no tickers to update
    return tickerslist #[row[0] for row in tickerslist[:10]]

def record_data(cur, all_companies:dict):
    
    for name,param in all_companies.items() :
     
            if param[5] == 0 or param[1] > param[5] : # [longName,currentPrice,currency, eps, bvps, gvalue]
                status = ticker_status.not_interesting.value
            else:
                status = ticker_status.interesting.value
        
            cur.execute('INSERT INTO tsx_stocks(ticker,fullname,price,currency,eps,bvps,truePrice,status) ' \
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (ticker) DO NOTHING',
            (name,param[0],param[1],param[2],param[3],param[4],param[5],status))
        # [longName,currentPrice,currency, eps, bvps, gvalue]

# удаление записи
def delete_record(cur,ticker:str):
    ticker = check_ticker_name(ticker)
    cur.execute('''DELETE FROM tsx_stocks WHERE ticker=%s''',(ticker,))
    return True        
# редактирование записи, иземенение статуса по тикеру
def edit_record(cur, ticker, status)->dict[str, Any]:
    cur.execute('''UPDATE tsx_stocks SET status=%s WHERE ticker=%s''',(status,ticker))
    cur.execute('''SELECT * FROM tsx_stocks WHERE ticker=%s''', (ticker,))
    row = cur.fetchone()
    return {
                'id': row[0],
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'truePrice': row[5], 
                'status': row[6]
                }
