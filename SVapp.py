from typing import Any

import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_svapp as db
import schemas
import stocks_valuation as sv

app = FastAPI()

#список тикеров для покупки
@app.get("/ticker/interesting_tickers", response_model=list[schemas.ticker_info])
def interesting_tickers():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.ineteresting_tickers(cur)

        return row

#список неинтересных тикеров для покупки
@app.get("/ticker/not_interesting_tickers", response_model=list[schemas.ticker_info])
def not_interesting_tickers():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.not_ineteresting_tickers(cur)

        return row

# инфо по тикеру
@app.get("/ticker/ticker_info/{ticker}", response_model=schemas.ticker_info| dict[str,Any])   
def ticker_info(ticker:str):
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.ticker_info(cur, ticker)
        return row

#добавление нового тикера
@app.post("/ticker/adding_ticker/{ticker}", response_model=schemas.ticker_info)
def adding_ticker(ticker:str):
        with db.get_db_connection() as conn, conn.cursor() as cur:
# def обработка тикера, сделать большими бувками и добаить .TO
            date_for_DB = sv.newticker_date(ticker)    
            row = db.save_new_ticker(cur, date_for_DB)
        return row

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