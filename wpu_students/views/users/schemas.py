from pydantic import BaseModel, field_validator, Field
import re


username_re = re.compile(r"^[a-z]+\.?[a-z]+$")
fullname_re = re.compile(r'^[A-Z][A-z\s]+$')


class BaseUser(BaseModel):
    username: str
    fullname: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, value):
        if not username_re.search(value):
            raise ValueError(
                "Username must contains only one dot and lower case characters")
        return value

    @field_validator('fullname')
    @classmethod
    def validate_fullname(cls, value: str):
        if not fullname_re.search(value):
            raise ValueError(
                "Fullname must contains only characters and spaces")
        return " ".join(re.findall(r'[A-z]+', value)).strip()


class AddUser(BaseUser):
    password: str = Field(str, min_length=8)


class EditUser(BaseUser):
    ...
