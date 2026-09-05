from typing import Any

import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_svapp as db
import schemas
import stocks_valuation as sv

app = FastAPI()

# @app.get("/ticker/droptable")
# def droptable():
#      with db.get_db_connection() as conn,conn.cursor() as cur:
#             db.drop_table(cur)
#      return {"status": "table dropped"}

# загрузка списка тикеров из файла, сбор данных по тикеру и запись в БД
# @app.post("/ticker/upload_tickers") 
# async def upload_tickers(): 
#     with db.get_db_connection() as conn, conn.cursor() as cur: 
#             file_name = 'list_of_tickers.txt' 
#             list_of_tickers = sv.upload_tickers_from_file(file_name) 
#             companies = await sv.companies_data(list_of_tickers) 
#             db.record_data(cur, companies) 
        
#     return {'status': 'data is loaded'}

#список тикеров для покупки
@app.get("/ticker/interesting_tickers", response_model=list[schemas.ticker_info])
def interesting_tickers():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        cur = conn.cursor()
        row = db.ineteresting_tickers(cur)

        return row

# инфо по тикеру
@app.get("/ticker/ticker_info/{ticker}", response_model=schemas.ticker_info| dict[str,Any])   
def ticker_info(ticker:str):
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #ticker = ticker.upper()
        row = db.ticker_info(cur, ticker)
        return row

#добавление нового тикера
@app.post("/ticker/create_ticker_in_db/{ticker}", response_model=schemas.ticker_info)
def create_ticker_in_db(ticker:str):
        with db.get_db_connection() as conn, conn.cursor() as cur:
# def обработка тикера, сделать большими бувками и добаить .TO
            date_for_DB = sv.newticker_date(ticker)    
            row = db.save_new_ticker(cur, date_for_DB)
        return row

  
#обновление статуса по тикерам, на усмотрение пользователя
# @app.patch("/ticker/update_status/{ticker}")
# def update_status(ticker:str,status:str):
#     with db.get_db_connection() as conn:
#         cur = conn.cursor()
#         row = db.edit_record(cur,ticker,status)
#         cur.close()
#         return row    

#удаление тикеров из БД
@app.delete("/ticker/delete_ticker/{ticker}")
def delete_ticker(ticker:str):
    with db.get_db_connection() as conn,conn.cursor() as cur:
       if not db.ticker_info(cur, ticker):
            return {'status':'ticker not found'}
       db.delete_record(cur,conn,ticker)
       return  {'status': 'ticker deleted'}

#docs
@app.get("/get_scalar_docs")
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API",
        )

@app.get("/")
def read_root():
    return {"status": "ok"}

        
# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("SVapp:app", host="127.0.0.1", port=8000, reload=True)