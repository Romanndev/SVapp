import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_sqlite as db
import schemas
import stocks_valuation as sv

app = FastAPI()

#обновление данных по всем тикерам в БД
@app.post("/ticker/update_all_tickers")
def update_all_tickers():
    with db.get_db_connection() as conn:
     cur = conn.cursor()
     db.update_all(cur)
    return {'status':'All data are updated'}

#список тикеров для покупки
@app.get("/ticker/tickers_for_buying", response_model=list[schemas.ticker_info])
def tickers_for_buying():
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.tickers_for_buying(cur)

        return row

#данные по тикеру
@app.get("/ticker/ticker_info_by_name/{ticker}", response_model=schemas.ticker_info)   
def ticker_info_by_name(ticker:str):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        ticker = ticker.upper()
        row = db.read_by_ticker(cur, ticker)
        return row

#добавление нового тикера        ДОРАБОТАЙ СО СБРОВ ПАРАМЕТРОВ АВТОМАТИЧЕСКИ, ПОЛУЧАТЬ ОТ ПОЛЬЗОВАТЕЛЯ ТИКЕР
@app.post("/ticker/create_ticker_in_db", response_model=schemas.ticker_info)
def create_ticker_in_db(ticker:schemas.Ticker):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.add_record(cur, conn, ticker)
        cur.close()
        return row

#загрузка списка тикеров из файла, сбор данных по тикеру и запись в БД
@app.post("/ticker/upload_tickers_from_file") 
def upload_tickers_from_file():
    with db.get_db_connection() as conn:
     cur = conn.cursor()
     file_name = 'list_of_tickers.txt'
     list_of_tickers = sv.upload_tickers_from_file(file_name)
     companies = sv.companies_data(list_of_tickers)
     sv.record_data(cur, companies)
     return {'status': 'data is loaded'} 
   
#обновление статуса по тикеры, на усмотрение пользователя
@app.patch("/ticker/update_status/{id}")
def update_status(id:int,status:str):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.edit_record(cur,id,status)
        cur.close()
        return row    

#удаление тикера из БД
@app.delete("/ticker/delete_ticker/{id}")
def delete_ticker(id):
    with db.get_db_connection() as conn:
       cur = conn.cursor()
       db.delete_record(cur,conn,id)
       cur.close()
       return  {'status': 'deleted'}

#docs
@app.get("/get_scalar_docs")
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API",
        )

#получение данных по тикеру по ID
#@app.get("/ticker/{id}", response_model=schemas.ticker_info)
#def get_ticker(id: int):
#    with db.get_db_connection() as conn:
#       cur = conn.cursor()
#       row = db.read_by_id(cur,id)
#       cur.close()
#       return row
        
# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("SVapp:app", host="127.0.0.1", port=8000, reload=True)