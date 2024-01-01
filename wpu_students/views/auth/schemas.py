from pydantic import BaseModel, Field, field_validator
import re


username_re = re.compile(r"^[a-z]+\.?[a-z]+$")


class UserLogin(BaseModel):
    username: str
    password: str = Field(str, min_length=8)

    @field_validator('username')
    @classmethod
    def validate_username(cls, value):
        if not username_re.search(value):
            raise ValueError(
                "Username must contains only one dot and lower case characters")
        return value
