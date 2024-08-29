from pydantic import BaseModel
from typing import List

class Flight(BaseModel):
    flight_num: str
    capacity: int
    estimated_flight_duration: int  

