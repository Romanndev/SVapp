#--------------------------------------------------------------------------------
# @app.get("/ticker/droptable")
# def droptable():
#      with db.get_db_connection() as conn,conn.cursor() as cur:
#             db.drop_table(cur)
#      return {"status": "table dropped"}
#--------------------------------------------------------------------------------
# загрузка списка тикеров из файла, сбор данных по тикеру и запись в БД
#--------------------------------------------------------------------------------
# @app.post("/ticker/upload_tickers") 
# async def upload_tickers(): 
#     with db.get_db_connection() as conn, conn.cursor() as cur: 
#             file_name = 'list_of_tickers.txt' 
#             list_of_tickers = sv.upload_tickers_from_file(file_name) 
#             companies = await sv.companies_data(list_of_tickers) 
#             db.record_data(cur, companies) 
        
#     return {'status': 'data is loaded'}

#--------------------------------------------------------------------------------
#обновление статуса по тикерам, на усмотрение пользователя
#--------------------------------------------------------------------------------
# @app.patch("/ticker/update_status/{ticker}")
# def update_status(ticker:str,status:str):
#     with db.get_db_connection() as conn:
#         cur = conn.cursor()
#         row = db.edit_record(cur,ticker,status)
#         cur.close()
#         return row 
#--------------------------------------------------------------------------------
# # чтение по ID - работа с БД
#--------------------------------------------------------------------------------
# def read_by_id(cur, id)->dict[str, Any]:
#     cur.execute('''SELECT * FROM Tickers WHERE id=%s''',(id,))
#     row = cur.fetchone()
#     return {
#             'id': row[0],
#             'ticker': row[1],
#             'fullname': row[2],
#             'price': row[3],
#             'currency': row[4],
#             'truePrice': row[5], 
#             'status': row[6]
#             }  