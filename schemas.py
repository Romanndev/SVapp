from datetime import date
from enum import Enum

from pydantic import BaseModel


class ticker_status(Enum):
    interesting = 'interesting'
    not_interesting = 'not interesting'


class ticker(BaseModel):
    ticker : str
    fullname : str
    price : float
    currency : str
    truePrice : float
    status : ticker_status

class ticker_info(ticker):
    id : int
    # ticker : str
    # fullname : str
    # price : float
    # currency : str
    # truePrice : float
    # status : ticker_status
    update_date : date
      

class newticker(ticker):
    eps : float
    bvps : float
