from datetime import date
from enum import Enum

from pydantic import BaseModel


class ticker_status(Enum):
    interesting = 'interesting'
    not_interesting = 'not interesting'
    
class ticker_info(BaseModel):
    id : int
    ticker : str
    fullname : str
    price : float
    currency : str
    truePrice : float
    status : ticker_status

class fulldate(ticker_info): 
    date : date   

class newticker(BaseModel):
    ticker : str
    fullname : str
    price : float
    currency : str
    truePrice : float
    status : ticker_status
