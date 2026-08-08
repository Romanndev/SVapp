from pydantic import BaseModel


class Ticker(BaseModel):
    id : int
    ticker : str
    fullname : str
    price : float
    currency : str
    truePrice : float
    status : str