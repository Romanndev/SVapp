# добавление нового тикера
# @app.post("/ticker/add_ticker/{ticker}", response_model=schemas.ticker_info | dict[str,str])
# def add_ticker(ticker:str):
#         ticker = db.check_ticker_name(ticker)
#         date_for_DB = sv.newticker_date(ticker) 
#         if date_for_DB.fullname == 'no date': 
#             return {'status':'Ticker data not found'}
        
#         with db.get_db_connection() as conn, conn.cursor() as cur:
#             row = db.save_new_ticker(cur, date_for_DB)
#         return row
 
# удаление тикера из БД
# @app.delete("/ticker/delete_ticker/{ticker}")
# def delete_ticker(ticker:str):
#     with db.get_db_connection() as conn,conn.cursor() as cur:
#         if not db.ticker_info(cur, ticker): return {'status':'ticker not found'}
#         if db.delete_record(cur,ticker) == True: return  {'status': 'ticker is deleted'}

# обновление данных по всем тикерам в БД 
# @app.patch("/ticker/update_tickers", response_model=dict[str,str]) 
# #async 
# def update_tickers(): 
#      with db.get_db_connection() as conn, conn.cursor() as cur:
#         #await db.update_all(cur)
#        db.updateSTATUS(cur)
#      return {'status':'tickers are updated'}

# тест гипотизы - данные из yfinance альтернативный путь
# @app.get("/ticker/test_update")
# def test_update():
#     with db.get_db_connection() as conn, conn.cursor() as cur:
#         sv.test_update(cur)
#     return {'price':'all good'}


#--------------------------------------------------------------------------------
# @app.get("/ticker/droptable")
# def droptable():
#      with db.get_db_connection() as conn,conn.cursor() as cur:
#             db.drop_table(cur)
#      return {"status": "table dropped"}
# #--------------------------------------------------------------------------------
# # загрузка списка тикеров из файла, сбор данных по тикеру и запись в БД
# #--------------------------------------------------------------------------------
# @app.get("/ticker/upload_tickers")
# def create_table():
#      with db.get_db_connection() as con:
#           print('УРААА')
      
# async def upload_tickers(): 
#     with db.get_db_connection() as conn, conn.cursor() as cur: 
#             file_name = 'list_of_tickers.txt' 
#             list_of_tickers = sv.upload_tickers_from_file(file_name) 
#             companies = await sv.companies_data(list_of_tickers) 
#             db.record_data(cur, companies) 
        
#     return {'status': 'data is loaded'}