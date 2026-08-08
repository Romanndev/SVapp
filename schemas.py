from pydantic import BaseModel


class Ticker(BaseModel):
    ticker : str
    fullname : str
    price : float
    currency : str
    truePrice : float
    status : str

class ticker_info(Ticker):
    id : int