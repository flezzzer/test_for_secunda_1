from typing import List, Optional
from pydantic import BaseModel

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    children: List["Activity"] = []
    class Config:
        orm_mode = True

Activity.update_forward_refs()
