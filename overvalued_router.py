
from typing import Any

from fastapi import APIRouter

import db_sv as db
import schemas

router = APIRouter()


#список переоцененных тикеров Financials
@router.get("/tsx_stocks/overvalued/Financials", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Financials():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Financials')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Basic Materials
@router.get("/tsx_stocks/overvalued/Basic_Materials", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Basic_Materials():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Basic Materials')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Energy
@router.get("/tsx_stocks/overvalued/Energy", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Energy():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Energy')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Industrials
@router.get("/tsx_stocks/overvalued/Industrials", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Industrials():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Industrials')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Consumer Discretionary
@router.get("/tsx_stocks/overvalued/Consumer_Discretionary", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Consumer_Discretionary():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Consumer Discretionary')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Consumer Staples
@router.get("/tsx_stocks/overvalued/Consumer_Staples", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Consumer_Staples():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Consumer Staples')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Health Care
@router.get("/tsx_stocks/overvalued/Health_Care", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Health_Care():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Health Care')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Technology
@router.get("/tsx_stocks/overvalued/Technology", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Technology():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Technology')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Telecommunications
@router.get("/tsx_stocks/overvalued/Telecommunications", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Telecommunications():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Telecommunications')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Utilities
@router.get("/tsx_stocks/overvalued/Utilities", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Utilities():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Utilities')
        if row == []: return {'status':'No tickers in the database'}
        return row

#список переоцененных тикеров Real Estate
@router.get("/tsx_stocks/overvalued/Real_Estate", response_model=list[schemas.ticker_info] | dict[str,Any])
def overvalued_Real_Estate():
    with db.get_db_connection() as conn, conn.cursor() as cur:
        row = db.overvalued_tickers(cur,'Real Estate')
        if row == []: return {'status':'No tickers in the database'}
        return row


