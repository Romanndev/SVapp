import os

#import sqlite3
from contextlib import contextmanager
from typing import Any

import psycopg2

import stocks_valuation as sv
from schemas import Ticker


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
        cur.execute('''CREATE TABLE IF NOT EXISTS Tickers (
                id SERIAL PRIMARY KEY,
                ticker TEXT UNIQUE,
                fullname TEXT,
                price REAL,
                currency TEXT,
                truePrice REAL, 
                status TEXT,
                data DATE DEFAULT CURRENT_TIMESTAMP)
                ''')
           
    except psycopg2.Error as e:
        raise psycopg2.OperationalError(f"Error, table creation: '{e}'")

#чтение по Name
def read_by_ticker(cur,ticker:str)->dict[str,Any]:
# доработать проверку на отсутствие тикера в БД  
    #ticker = sv.check_ticker_name(ticker)  
    cur.execute('''SELECT * FROM Tickers WHERE ticker=%s''',(ticker,))
    
    row =cur.fetchone()
    if row is None:
        return {
                'id': None,
                'ticker': None,
                'fullname': None,
                'price': None,
                'currency': None,
                'truePrice': None, 
                'status': None
                }
    # cur.execute("SELECT COUNT(*) FROM Tickers;")
    # count = cur.fetchone()[0]
    # print(count)
    else :
        return {
                'id': row[0],
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'truePrice': row[5], 
                'status': row[6]
                }

# добавление новой записи
def add_record(cur, conn, ticker: Ticker)->dict[str, Any]:
    ticker_lable = ticker.ticker
    fullname = ticker.fullname
    price = ticker.price
    currency = ticker.currency
    trueprice = ticker.truePrice
    status = ticker.status

    cur.execute('''INSERT INTO Tickers(ticker, fullname, price, currency, truePrice, status) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (ticker) DO NOTHING''', (ticker_lable, fullname, price, currency, trueprice, status))
    cur.execute('''SELECT * FROM Tickers WHERE ticker=%s''',(ticker_lable,))
    row = cur.fetchone() 
    conn.commit()
    return {
                'id': row[0],
                'ticker': row[1],
                'fullname': row[2],
                'price': row[3],
                'currency': row[4],
                'truePrice': row[5], 
                'status': row[6]
                }

# редактирование записи, иземенение статусапо тикеру
def edit_record(cur, ticker, status)->dict[str, Any]:
    cur.execute('''UPDATE Tickers SET status=%s WHERE ticker=%s''',(status,ticker))
    cur.execute('''SELECT * FROM Tickers WHERE ticker=%s''', (ticker,))
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

# удаление записи по ID
def delete_record(cur,conn,ticker:str):
    cur.execute('''DELETE FROM Tickers WHERE ticker=%s''',(ticker,))
    conn.commit()

#тикеры для покупки
def tickers_for_buying(cur)->list[dict[str,Any]]:
    cur.execute('''SELECT * FROM Tickers WHERE status=%s''',('YES',))
    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({
                    'id': row[0],
                    'ticker': row[1],
                    'fullname': row[2],
                    'price': row[3],
                    'currency': row[4],
                    'truePrice': row[5], 
                    'status': row[6]
                    })

    return result    

#обновление данных по все тикерам в БД
async def update_all(cur):
    tickers_lable = []
    company_data = {}
    
    cur.execute('''SELECT ticker FROM Tickers''')
    for i in cur.fetchall():
      tickers_lable.append(i[0])

    company_data = await sv.companies_data(tickers_lable)
    for ticker, param in company_data.items():  
        if  param[5] is None or param[1] is None:
            cur.execute('''UPDATE Tickers SET price=%s,truePrice=%s,status=%s WHERE ticker=%s''',(param[1],param[5],'NO',ticker))

        elif param[1]< param[5]:
            cur.execute('''UPDATE Tickers SET price=%s,truePrice=%s,status=%s WHERE ticker=%s''',(param[1],param[5],'YES',ticker))

        elif param[1]> param[5]:
                    cur.execute('''UPDATE Tickers SET price=%s,truePrice=%s,status=%s WHERE ticker=%s''',(param[1],param[5],'NO',ticker))  


        
# чтение по ID
def read_by_id(cur, id)->dict[str, Any]:
    cur.execute('''SELECT * FROM Tickers WHERE id=%s''',(id,))
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