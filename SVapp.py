from typing import Any

import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_svapp as db
import schemas

app = FastAPI()

#список интересных тикеров для покупки
@app.get("/tsx_stocks/fair_value", response_model=list[schemas.ticker])
def fair_value():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.fair_value_tickers(cur)

        return row

#список не интересных тикеров для покупки
@app.get("/tsx_stocks/overvalued", response_model=list[schemas.ticker])
def overvalued():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur)

        return row

# инфо по тикеру
@app.get("/tsx_stocks/ticker_info/{ticker}", response_model=schemas.ticker | dict[str,Any])   
def ticker_info(ticker:str):
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.ticker_info(cur, ticker)
        if row == None: return {'status':'no ticker in the database'}
        return row
        
#docs
@app.get("/get_scalar_docs")
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API",
        )

#
@app.get("/")
def read_root():
    return {"status": "ok"}


# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("SVapp:app", host="127.0.0.1", port=8000, reload=True)