from pydantic import BaseModel, ConfigDict, Field, EmailStr

class UserBase(BaseModel):
    first_name: str = Field(..., json_schema_extra={"example": "Ivan"})
    last_name: str = Field(..., json_schema_extra={"example": "Ivanov"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ivan@mail.ru"})

class UserCreate(UserBase):
    pass

class UserInfo(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)
