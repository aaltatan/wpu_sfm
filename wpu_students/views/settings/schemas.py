from pydantic import BaseModel, Field


class ServiceSchema(BaseModel):
    name: str = Field(min_length=4)
    price: int = Field(gt=0)
