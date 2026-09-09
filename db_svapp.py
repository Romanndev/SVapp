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
                truePrice FLOAT4,
                status STRING,
                update_date DATE DEFAULT current_timestamp():::DATE,
                CONSTRAINT tsx_stocks_pkey PRIMARY KEY (id ASC)
                )"""
                    )
           
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
                    'id': row[0],
                    'ticker': row[1],
                    'fullname': row[2],
                    'price': row[3],
                    'currency': row[4],
                    'truePrice': row[5],
                    'status': row[6],
                    'update_date': row[7]
                    
                    })
    
    return  result

# неинтересные тикеры для покупки
def not_ineteresting_tickers(cur)->list[dict[str,Any]]:
    result = []
    cur.execute('''SELECT * FROM tsx_stocks WHERE status=%s''',(ticker_status.not_interesting.value,))
    rows = cur.fetchall()
    
    for row in rows:
        result.append({
                    'id': row[0],
                    'ticker': row[1],
                    'fullname': row[2],
                    'price': row[3],
                    'currency': row[4],
                    'truePrice': row[5],
                    'status': row[6],
                    'update_date': row[7]
                    
                    })
    
    return  result

# информация по тикеру
def ticker_info(cur,ticker:str)->dict[str,Any]: 
    ticker = sv.check_ticker_name(ticker)  
    cur.execute('''SELECT * FROM tsx_stocks WHERE ticker=%s''',(ticker,))
    row =cur.fetchone()
        
    if row is None:
        return {
                'status':'no ticker in the database'
                }
    
    return {
                'id': row[0],
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'truePrice': row[5], 
                'status': row[6],
                'update_date': row[7]
                }

# добавление нового тикера в БД
def save_new_ticker(cur, newticker_date: schemas.newticker)->dict[str, Any]:
    ticker = newticker_date.ticker
    fullname = newticker_date.fullname
    price = newticker_date.price
    currency = newticker_date.currency
    trueprice = newticker_date.truePrice
    status = newticker_date.status.value

    cur.execute('''INSERT INTO tsx_stocks(ticker, fullname, price, currency, truePrice, status) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (ticker) DO NOTHING''', (ticker, fullname, price, currency, trueprice, status))
    cur.execute('''SELECT * FROM tsx_stocks WHERE ticker=%s''',(ticker,))
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

# удаление записи
def delete_record(cur,conn,ticker:str):
    cur.execute('''DELETE FROM tsx_stocks WHERE ticker=%s''',(ticker,))
    conn.commit()
 
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
    count = 0
    tickerslist : list[str] = []
    cur.execute('''SELECT ticker FROM tsx_stocks WHERE update_date < %s''',(current_date,))
    if cur.fetchall() is None or len(cur.fetchall()) == 0: return tickerslist # empty list if no tickers to update
    for i in cur.fetchall():
        tickerslist.append(i)
        if count == 10 :  break
        else:  count = count + 1

    return tickerslist

def record_data(cur, all_companies:dict):
    
    for name,param in all_companies.items() :
     
            if param[5] == 0 or param[1] > param[5] : # [longName,currentPrice,currency, eps, bvps, gvalue]
                status = ticker_status.not_interesting.value
            else:
                status = ticker_status.interesting.value
        
            cur.execute('INSERT INTO tsx_stocks(ticker,fullname,price,currency,truePrice,status) ' \
            'VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (ticker) DO NOTHING',
            (name,param[0],param[1],param[2],param[5],status))
        # [longName,currentPrice,currency, eps, bvps, gvalue]

        
