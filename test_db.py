import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_sqlite as db
import schemas
import stocks_valuation as sv

app = FastAPI()


@app.get("/ticker/ticker_name/{ticker}", response_model=schemas.ticker_info)   
def get_ticker_by_name(ticker:str):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        ticker = ticker.upper()
        row = db.read_by_ticker(cur, ticker)

        return row

@app.get("/ticker/tickers_for_Buying", response_model=list[schemas.ticker_info])
def tickers_for_buying():
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.tickers_for_buying(cur)

        return row


        
@app.post("/ticker/create", response_model=schemas.ticker_info)
def create_ticker(ticker:schemas.Ticker):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.add_record(cur, conn, ticker)
        cur.close()

        return row

@app.post("/ticker/upload_from_file") 
def upload_tickers():
    with db.get_db_connection() as conn:
     cur = conn.cursor()
     file_name = 'list_of_tickers.txt'
     list_of_tickers = sv.upload_tickers_from_file(file_name)
     companies = sv.companies_data(list_of_tickers)
     sv.record_data(cur, companies)

     return {'status': 'data is loaded'} 
     
#обновление данных по всем тикерам в БД
@app.post("/ticker/update_all")
def update_all_tickers():
    with db.get_db_connection() as conn:
     cur = conn.cursor()
     db.update_all(cur)

    return {'status':'All data are updated'}
     




@app.patch("/ticker/update/{status}")
def update_status(id:int,status:str):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.edit_record(cur,id,status)
        cur.close()
        return row    

@app.delete("/ticker/delete/{id}")
def delete_ticker(id):
    with db.get_db_connection() as conn:
       cur = conn.cursor()
       db.delete_record(cur,conn,id)
       cur.close()
       return  {'status': 'deleted'}

#docs
@app.get("/scalar")
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API",
        )

#ticker по ID
@app.get("/ticker/{id}", response_model=schemas.ticker_info)
def get_ticker(id: int):
    with db.get_db_connection() as conn:
       cur = conn.cursor()
       row = db.read_by_id(cur,id)
       cur.close()
       return row
        
# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("test_db:app", host="127.0.0.1", port=8000, reload=True)