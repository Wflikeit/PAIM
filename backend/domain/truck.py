from typing import List

from pydantic import BaseModel
from pydantic.v1 import Field


class Truck(BaseModel):
    registration_number: str
    orders: List[str] = Field(default_factory=list)
    warehouse: str
