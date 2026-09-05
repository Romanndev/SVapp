import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_svapp as db
import schemas
import stocks_valuation as sv

app = FastAPI()

@app.get("/ticker/droptable")
def droptable():
     with db.get_db_connection() as conn:
          cur = conn.cursor()
          db.drop_table(cur)
          cur.close()
          
          return {"status": "table dropped"}

#список тикеров для покупки
@app.get("/ticker/tickers_for_buying", response_model=list[schemas.ticker_info])
def tickers_for_buying():
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.tickers_for_buying(cur)

        return row

#данные по тикерам
@app.get("/ticker/ticker_info_by_name/{ticker}", response_model=schemas.ticker_info)   
def ticker_info_by_name(ticker:str):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        ticker = ticker.upper()
        row = db.read_by_ticker(cur, ticker)
        return row

#добавление нового тикера
@app.post("/ticker/create_ticker_in_db/{ticker}", response_model=schemas.ticker_info)
def create_ticker_in_db(ticker:str):
        with db.get_db_connection() as conn:
            cur = conn.cursor()
# def обработка тикера, сделать большими бувками и добаить .TO
            date_for_DB = sv.ticker_full_date_for_DB(ticker)    
            row = db.add_record(cur, conn, date_for_DB)
            cur.close()
        return row

  
#обновление статуса по тикерам, на усмотрение пользователя
@app.patch("/ticker/update_status/{ticker}")
def update_status(ticker:str,status:str):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.edit_record(cur,ticker,status)
        cur.close()
        return row    

#удаление тикеров из БД
@app.delete("/ticker/delete_ticker/{ticker}")
def delete_ticker(ticker:str):
    with db.get_db_connection() as conn:
       cur = conn.cursor()
       db.delete_record(cur,conn,ticker)
       cur.close()
       return  {'status': 'deleted'}

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