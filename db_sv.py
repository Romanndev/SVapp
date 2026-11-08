import datetime
import os

#import sqlite3
from contextlib import contextmanager
from typing import Any
from zoneinfo import ZoneInfo

import psycopg2

import engine_sv as sv
import schemas
from schemas import ticker_status


@contextmanager
def get_db_connection():
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
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
                CONSTRAINT tsx_stocks_pkey PRIMARY KEY (id ASC),
                sector STRING
                )"""
                    ) # [longName,currentPrice,currency, eps, bvps, gvalue, sector]
           
    except psycopg2.Error as e:
        raise psycopg2.OperationalError(f"Error, table creation: '{e}'")

# удаление таблицы
def drop_table(cur):
    cur.execute('''DROP TABLE IF EXISTS tsx_stocks CASCADE''')

# интересные тикеры для покупки (по сектору) (Financials, Energy, Basic Materials, Industrials, Consumer Discretionary, Consumer Staples, Health Care, Information Technology, Communication Services, Utilities, Real Estate)
def fair_value_tickers(cur, sector:str)->list[dict[str,Any]]:
    result = []
    cur.execute('''SELECT * FROM tsx_stocks WHERE status=%s AND sector=%s''',(ticker_status.fair_value.value, sector))
    rows = cur.fetchall()
    
    for row in rows:
        result.append({
                    #'id': row[0],
                    'ticker': row[1],
                    'fullname': row[2],
                    'price': row[3],
                    'currency': row[4],
                    'true_price': row[7],
                    'status': row[8],
                    'update_date': row[9],
                    'sector': row[10]
                    })
    
    return  result

# НЕ интересные тикеры для покупки
def overvalued_tickers(cur, sector:str)->list[dict[str,Any]]:
    result = []
    cur.execute('''SELECT * FROM tsx_stocks WHERE status=%s AND sector=%s''',(ticker_status.overvalued.value, sector))
    rows = cur.fetchall()
    
    for row in rows:
        result.append({
                    #'id': row[0],
                    'ticker': row[1],
                    'fullname': row[2],
                    'price': row[3],
                    'currency': row[4],
                    'true_price': row[7],
                    'status': row[8],
                    'update_date': row[9],
                    'sector': row[10]
                    
                    })
    
    return  result

def check_ticker_name(ticker)-> str:
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
    
    return {    #'id': row[0],
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'true_price': row[7],
                'status': row[8],
                'update_date': row[9],
                'sector': row[10]
                }

# добавление нового тикера в БД
def save_new_ticker(cur, newticker_date: schemas.newticker)->dict[str, Any]:
    ticker = newticker_date.ticker
    fullname = newticker_date.fullname
    price = newticker_date.price
    currency = newticker_date.currency
    eps = newticker_date.eps
    bvps = newticker_date.bvps
    true_price = newticker_date.truePrice
    status = newticker_date.status.value

    cur.execute('''INSERT INTO tsx_stocks(ticker, fullname, price, currency,eps,bvps,true_price, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (ticker) DO NOTHING''', (ticker, fullname, price, currency,eps,bvps,true_price, status))
    cur.execute('''SELECT * FROM tsx_stocks WHERE ticker=%s''',(ticker,))
    row = cur.fetchone() 
    
    return {
                'id': row[0],
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'true_price': row[7], 
                'status': row[8],
                'update_date': row[9]
                }

#обновление данных по всем тикерам в БД (tsx_stocks) по актуальной ЦЕНЕ на ДАТУ
def update_tsx_stocks(cur):
    tickerslist = []
    company_prices = {}

    current_date = datetime.datetime.now(ZoneInfo("America/Edmonton")).date()
    cur.execute('''SELECT update_date FROM tsx_stocks''')
    last_update = cur.fetchone() 
    if last_update is not None and last_update[0] == current_date: return 

    tickerslist = tickers_for_update(cur,current_date)
    if tickerslist :
         company_prices = sv.tsx_prices(tickerslist)
    # id, ticker,fullname,price,currency,eps,bvps,truePrice,status,update_date
         for i in tickerslist:
            cur.execute(
                        '''UPDATE tsx_stocks SET price=%s,update_date=%s WHERE ticker=%s''',
                                (company_prices[i],current_date,i)
                                )
            cur.execute('''SELECT truePrice FROM tsx_stocks WHERE ticker=%s''',(i,))
            true_price = cur.fetchone() # gvalue
            if true_price is None: continue
            if company_prices[i] > true_price[0]:
                cur.execute(
                            '''UPDATE tsx_stocks SET status=%s WHERE ticker=%s''',(ticker_status.overvalued.value,i)
                        )
            if company_prices[i] <= true_price[0]:    
                cur.execute(
                            '''UPDATE tsx_stocks SET status=%s WHERE ticker=%s''',(ticker_status.fair_value.value,i)
                        )
          
# список тикеров для обновления данных на текущую дату
def tickers_for_update(cur,current_date)->list[str]:
    tickerslist = []
    cur.execute('''SELECT ticker FROM tsx_stocks WHERE update_date < %s''',(current_date,))
    rows = cur.fetchall()
    tickerslist = [i[0] for i in rows]
    if tickerslist is None or len(tickerslist) == 0: 
        return [] # empty list if no tickers to update
    
    return tickerslist

# удаление записи
def delete_record(cur,ticker:str):
    ticker = check_ticker_name(ticker)
    if cur.execute('''DELETE FROM tsx_stocks WHERE ticker=%s''',(ticker,)): return True        

# добавление новой колонки в таблицу
def add_column(cur,column_name:str,column_type: Any):
    try:
        cur.execute(f'''ALTER TABLE tsx_stocks ADD COLUMN IF NOT EXISTS {column_name} {column_type}''')
    except psycopg2.Error as e:
        raise psycopg2.OperationalError(f"Error, adding column: '{e}'")

# редактирование sector для тикера
def edit_record(cur,ticker:str,sector:str):
    ticker = check_ticker_name(ticker)
    cur.execute('''UPDATE tsx_stocks SET sector=%s WHERE ticker=%s''',(sector,ticker))
    cur.execute('''SELECT * FROM tsx_stocks WHERE ticker=%s''',(ticker,))
    row = cur.fetchone()
    return {
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'true_price': row[7], 
                'status': row[8],
                'update_date': row[9],
                'sector': row[10]
    }