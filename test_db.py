import uvicorn
from fastapi import FastAPI

import db_sqlite as db
import schemas

app = FastAPI()

@app.get("/shipment/{ticker_id}", response_model=schemas.ticker_info)
def get_ticker(ticker_id: int):
    with db.get_db_connection() as conn:
       cur = conn.cursor()
       row = db.read_by_id(cur,ticker_id)
       return row
        
@app.post("/shipment/", response_model=schemas.ticker_info)
def create_ticker(ticker:schemas.Ticker):
    with db.get_db_connection() as conn:
        cur = conn.cursor()
        row = db.add_record(cur, conn, ticker)
        return row

@app.delete("/shipment/{ticker_id}")
def delete_ticker(ticker_id):
    with db.get_db_connection() as conn:
       cur = conn.cursor()
       db.delete_record(cur,conn,ticker_id)
       return  {'status': 'deleted'}
# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("test_db:app", host="127.0.0.1", port=8000, reload=True)