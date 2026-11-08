from typing import Any

import uvicorn
from fastapi import FastAPI

#from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

import db_sv as db
import fair_router as fr
import overvalued_router as ovrr
import schemas
import update_router as ur

app = FastAPI(title="Stock Valuation App", description="API for Stock Valuation App", version="1.0.0")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://svapp-web.onrender.com"],  # Или укажите точный URL вашего фронтенда на Render
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(fr.router, tags=["tsx_stocks fair value"])
app.include_router(ovrr.router, tags=["tsx_stocks overvalued"])
app.include_router(ur.router, prefix="/update", tags=["update"])





# инфо по тикеру
# @app.get("/tsx_stocks/ticker_info/{ticker}", tags=["tsx_stocks"],response_model=schemas.ticker_info | dict[str,Any])   
# def ticker_info(ticker:str):
#     with db.get_db_connection() as conn, conn.cursor() as cur:
#         db.update_tsx_stocks(cur)
#         row = db.ticker_info(cur, ticker)
#         if row == None: return {'status':'no ticker in the database'}
#         return row
        
#docs
@app.get("/get_scalar_docs", tags=["docs"])
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API",
        )

# @app.get("/", tags=["root"])
# def read_root():
#     return {"status": "ok"}

@app.get("/health", tags=["root"])
def health_check():
    return {"status": "healthy"}


# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)