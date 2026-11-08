from typing import Any

from fastapi import APIRouter

import db_sv as db
import schemas

router = APIRouter()

# список справедливых тикеров Financials
@router.get("/tsx_stocks/fair_value/Financials", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Financials():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Financials')
        return row

# список справедливых тикеров Basic Materials
@router.get("/tsx_stocks/fair_value/Basic_Materials", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Basic_Materials():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Basic Materials')
        if row == []: return {'status':'no tickers in the database'}
        return row

# список справедливых тикеров Energy
@router.get("/tsx_stocks/fair_value/Energy", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Energy():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Energy')
        if row == []: return {'status':'no tickers in the database'}
        return row  

# список справедливых тикеров Industrials
@router.get("/tsx_stocks/fair_value/Industrials", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Industrials():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Industrials')
        if row == []: return {'status':'no tickers in the database'}
        return row 

# список справедливых тикеров Consumer Discretionary
@router.get("/tsx_stocks/fair_value/Consumer Discretionary", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Consumer_Discretionary():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Consumer Discretionary')
        if row == []: return {'status':'no tickers in the database'}
        return row 

# список справедливых тикеров Consumer Staples
@router.get("/tsx_stocks/fair_value/Consumer Staples", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Consumer_Staples():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Consumer Staples')
        if row == []: return {'status':'no tickers in the database'}
        return row 

# список справедливых тикеров Health Care
@router.get("/tsx_stocks/fair_value/Health Care", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Health_Care():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Health Care')
        if row == []: return {'status':'no tickers in the database'}
        return row

# список справедливых тикеров Technology
@router.get("/tsx_stocks/fair_value/Technology", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Technology():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Technology')
        if row == []: return {'status':'no tickers in the database'}
        return row 

# список справедливых тикеров Telecommunications
@router.get("/tsx_stocks/fair_value/Telecommunications", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Telecommunications():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Telecommunications')
        if row == []: return {'status':'no tickers in the database'}
        return row 

# список справедливых тикеров Utilities
@router.get("/tsx_stocks/fair_value/Utilities", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Utilities():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Utilities')
        if row == []: return {'status':'no tickers in the database'}
        return row

# список справедливых тикеров Real Estate
@router.get("/tsx_stocks/fair_value/Real Estate", response_model=list[schemas.ticker_info] | dict[str,Any])
def fair_value_Real_Estate():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        #db.update_tsx_stocks(cur)
        row = db.fair_value_tickers(cur, 'Real Estate')
        if row == []: return {'status':'no tickers in the database'}
        return row 