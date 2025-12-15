from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass   # user_id сюда больше не передаём

class TagUpdate(BaseModel):
    name: str | None = None 

class TagOut(TagBase):
    id: int
    user_id: int   # он есть в ответе, чтобы видеть чей тег

    class Config:
        from_attributes = True
