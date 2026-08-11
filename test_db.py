import uvicorn
from fastapi import FastAPI

import db_sqlite as db
import schemas
import stocks_valuation as sv

app = FastAPI()

@app.get("/ticker/{id}", response_model=schemas.ticker_info)
def get_ticker(id: int):
    with db.get_db_connection() as conn:
       cur = conn.cursor()
       row = db.read_by_id(cur,id)
       cur.close()
       return row
        
@app.post("/ticker/create", response_model=schemas.ticker_info)
def create_ticker(ticker:schemas.Ticker):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.add_record(cur, conn, ticker)
        cur.close()

        return row

@app.post("/ticker/upload_from_file") 
def upload():
    with db.get_db_connection() as conn:
     cur = conn.cursor()
     file_name = 'list_of_tickers.txt'
     list_of_tickers = sv.upload_tickers_from_file(file_name)
     companies = sv.companies_data(list_of_tickers)
     sv.record_data(cur, companies)

     return {'status': 'data is loaded'} 
     

#@app.post("/ticker/update_all")

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
# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("test_db:app", host="127.0.0.1", port=8000, reload=True)