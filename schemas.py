from pydantic import BaseModel


class Ticker(BaseModel):
    ticker : str | None
    fullname : str | None
    price : float | None
    currency : str | None
    truePrice : float | None
    status : str | None

class ticker_info(Ticker):
    id : int