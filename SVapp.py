from typing import Any

import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_svapp as db
import schemas
import stocks_valuation as sv

app = FastAPI()

#список интересных тикеров для покупки
@app.get("/ticker/interesting_tickers", response_model=list[schemas.ticker_info])
def interesting_tickers():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.ineteresting_tickers(cur)

        return row

#список не интересных тикеров для покупки
@app.get("/ticker/not_interesting_tickers", response_model=list[schemas.ticker_info])
def not_interesting_tickers():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.not_ineteresting_tickers(cur)

        return row

# инфо по тикеру
@app.get("/ticker/ticker_info/{ticker}", response_model=schemas.ticker_info | dict[str,Any])   
def ticker_info(ticker:str):
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.ticker_info(cur, ticker)
        if row == None: return {'status':'no ticker in the database'}
        return row

#добавление нового тикера
# @app.post("/ticker/add_ticker/{ticker}", response_model=schemas.ticker_info)
# def add_ticker(ticker:str):
#         with db.get_db_connection() as conn, conn.cursor() as cur:
#             ticker = db.check_ticker_name(ticker)
#             date_for_DB = sv.newticker_date(ticker)    
#             row = db.save_new_ticker(cur, date_for_DB)
#         return row

#удаление тикера из БД
# @app.delete("/ticker/delete_ticker/{ticker}")
# def delete_ticker(ticker:str):
#     with db.get_db_connection() as conn,conn.cursor() as cur:
#         if not db.ticker_info(cur, ticker): return {'status':'ticker not found'}
#         if db.delete_record(cur,ticker) == True: return  {'status': 'ticker is deleted'}

# обновление данных по всем тикерам в БД 
# @app.patch("/ticker/update_tickers", response_model=dict[str,str]) 
# async def update_tickers(): 
#      with db.get_db_connection() as conn, conn.cursor() as cur:
#         await db.update_all(cur)

#      return {'status':'tickers are updated'}

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

#--------------------------------------------------------------------------------
# @app.get("/ticker/droptable")
# def droptable():
#      with db.get_db_connection() as conn,conn.cursor() as cur:
#             db.drop_table(cur)
#      return {"status": "table dropped"}
# #--------------------------------------------------------------------------------
# # загрузка списка тикеров из файла, сбор данных по тикеру и запись в БД
# #--------------------------------------------------------------------------------
# @app.post("/ticker/upload_tickers") 
# async def upload_tickers(): 
#     with db.get_db_connection() as conn, conn.cursor() as cur: 
#             file_name = 'list_of_tickers.txt' 
#             list_of_tickers = sv.upload_tickers_from_file(file_name) 
#             companies = await sv.companies_data(list_of_tickers) 
#             db.record_data(cur, companies) 
        
#     return {'status': 'data is loaded'}
        
# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("SVapp:app", host="127.0.0.1", port=8000, reload=True)