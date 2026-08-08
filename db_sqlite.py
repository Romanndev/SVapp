import sqlite3
from contextlib import contextmanager

from schemas import Ticker


@contextmanager
def get_db_connection():
        conn = sqlite3.connect('tickers.db')
        create_table(conn.cursor())
        yield conn
        conn.commit()
        conn.close()
        


#создание,подключение к базе данных
#def create_db():
##    conn = sqlite3.connect('tickers.db')
#    cur = conn.cursor()
#    return cur

# создание таблицы
def create_table(cur):
    try :
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
    
    except sqlite3.Error as e:
        print(f"Error, table creation: {e}")

# чтение по ID
def read_by_id(cur, id):
    cur.execute('''SELECT * FROM Tickers WHERE id=?''',(id,))
    row = cur.fetchone()
    return row

# добавление записи по ID
def add_record(cur, conn, ticker: Ticker):
    ticker_lable = ticker.ticker
    fullname = ticker.fullname
    price = ticker.price
    currency = ticker.currency
    trueprice = ticker.truePrice
    status = ticker.status

    cur.execute('''INSERT OR IGNORE INTO Tickers(ticker, fullname, price, currency, truePrice, status) VALUES (?,?,?,?,?,?)''', (ticker_lable, fullname, price, currency, trueprice, status))
    cur.execute('''SELECT * FROM Tickers WHERE ticker=?''',(ticker_lable,))
    row = cur.fetchone() 
    conn.commit()
    
    return row

# редактирование записи по ID
#def edit_record(cur, id, ticker_date :Ticker):

# обновление всех записей в таблице
#def update_all_date(cur, all_companies):

# удаление записи по ID
def deelete_record(cur,conn, id):
    cur.exeute('''DELETE FROM Tickers WHERE id=?''',(id,))
    conn.commit()

    return {'status': f'row with {id} deleted'}

# запись и закрытие базы данных
def save_an_close_db(cur, conn):
    conn.commit()
    cur.close()
    conn.close()


# сохранить полученные данные и оценку привлекательности к покупке тикеров 
# save the obtained data and the assessment of the attractiveness of purchasing tickers

    

    

#    for name,param in all_companies.items() :
# 
#        if param[5] is None or param[1] > param[5] :
#            status = 'NO'
#        else:
#            status = 'YES'
#    
#        cur.execute('INSERT OR IGNORE INTO Tickers(id,ticker,fullname,price,currency,truePrice,status) VALUES (?,?,?,?,?,?,?)',(None,name,param[0],param[1],param[2],param[5],status))
# 
#
#    conn.commit()
#    conn.close()