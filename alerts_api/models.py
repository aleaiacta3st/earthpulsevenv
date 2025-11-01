from datetime import datetime
from pydantic import BaseModel

class Earthquake(BaseModel):
    id :str
    place:str
    magnitude:float
    depth:float
    latitude:float
    longitude:float
    tsunami:bool
    occurred_at:datetime