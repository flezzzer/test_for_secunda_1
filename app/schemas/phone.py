from pydantic import BaseModel

class Phone(BaseModel):
    id: int
    number: str
    class Config:
        orm_mode = True
