from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import List
import re


class RowReceipt(BaseModel):
    service_id: int = Field(int, alias='serviceId')
    quantity: int = Field(int, alias='qt', gt=0)
    price: int = Field(gt=0)
    notes: str | None = None


class ReceiptSchema(BaseModel):
    user_id: int = Field(int, alias='userId')
    date: str | datetime
    client_id: str = Field(alias='id')
    client: str = Field(str, alias='clientName', min_length=2)
    faculty_id: int = Field(int, alias='faculty')
    notes: str | None = None
    rows: List[RowReceipt] = Field(min_length=1)

    @field_validator('client_id')
    @classmethod
    def validate_id(cls, value):
        if value:
            regex = re.compile(r"^20[1-2]\d{6}$")
            criteria = regex.search(value)
            if criteria:
                return value
            else:
                raise ValueError("Client id is not valid!")
        else:
            return None

    @field_validator('date')
    @classmethod
    def validate_date(cls, value):
        try:
            date = datetime.strptime(value, r"%Y-%m-%d")
        except:
            raise ValueError("Please input a valid date")
        return date
