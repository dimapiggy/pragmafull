from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    id: int
    telegram_id: int
    username: str | None = None
    fullname: str | None = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str | None = None
    fullname: str | None = None

class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
