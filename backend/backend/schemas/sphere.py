from pydantic import BaseModel

class SphereBase(BaseModel):
    name: str

class SphereCreate(SphereBase):
    pass

class SphereUpdate(BaseModel):
    name: str | None = None 

class SphereOut(SphereBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


