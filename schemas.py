from datetime import date
from enum import Enum

from pydantic import BaseModel


class ticker_status(Enum):
    fair_value = 'fair value'
    overvalued = 'overvalued'
  

class ticker(BaseModel):
    ticker : str
    fullname : str
    price : float
    currency : str
    true_price : float
    status : ticker_status

class ticker_info(ticker):
    #id : int
    # ticker : str
    # fullname : str
    # price : float
    # currency : str
    # true_price : float
    # status : ticker_status
    update_date : date
    sector : str
      

class newticker(ticker):
    eps : float
    bvps : float

class ticker_sector(Enum):
    telecommunications = 'Telecommunications'
    financials = 'Financials'
    technology = 'Technology'
    energy = 'Energy'
    industrials = 'Industrials'
    basic_materials = 'Basic Materials'
    consumer_discretionary = 'Consumer Discretionary'
    consumer_staples = 'Consumer Staples'
    health_care = 'Health Care'
    utilities = 'Utilities'
    real_estate = 'Real Estate'
