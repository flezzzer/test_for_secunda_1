from typing import List
from pydantic import BaseModel, Field
from app.schemas.building import Building
from app.schemas.activity import Activity
from app.schemas.phone import Phone

class OrganizationBase(BaseModel):
    name: str
    building_id: int
    phone_numbers: List[str] = Field(default_factory=list)
    activity_ids: List[int] = Field(default_factory=list)

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    phones: List[Phone]
    activities: List[Activity]
    building: Building

    class Config:
        orm_mode = True
