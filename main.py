from typing import Any

import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

import db_sv as db
import schemas
import update_router as ur

app = FastAPI(title="Stock Valuation App", description="API for Stock Valuation App", version="1.0.0")


#список справедливых тикеров
@app.get("/tsx_stocks/fair_value", tags=["tsx_stocks"], response_model=list[schemas.ticker_info])
def fair_value():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur)

        return row

#список переоцененных тикеров
@app.get("/tsx_stocks/overvalued", tags=["tsx_stocks"], response_model=list[schemas.ticker_info])
def overvalued():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        db.update_tsx_stocks(cur)
        row = db.overvalued_tickers(cur)

        return row

# инфо по тикеру
@app.get("/tsx_stocks/ticker_info/{ticker}", tags=["tsx_stocks"],response_model=schemas.ticker_info | dict[str,Any])   
def ticker_info(ticker:str):
    with db.get_db_connection() as conn, conn.cursor() as cur:
        db.update_tsx_stocks(cur)
        row = db.ticker_info(cur, ticker)
        if row == None: return {'status':'no ticker in the database'}
        return row
        
#docs
@app.get("/get_scalar_docs", tags=["tsx_stocks"])
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API",
        )

@app.get("/", tags=["tsx_stocks"])
def read_root():
    return {"status": "ok"}

# app.include_router(ur.router, prefix="/update", tags=["update"])


# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)