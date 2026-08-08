from fastapi import FastAPI

import db_sqlite



app = FastAPI()

@app.get("/get_ticker/{ticker_id}")
def get_ticker(ticker_id: int):

    with db_sqlite.get_db_connection as con:
        

    