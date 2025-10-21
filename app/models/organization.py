from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.db import Base

org_activity = Table(
    "org_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
)

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="SET NULL"))

    building = relationship("Building", back_populates="organizations")
    phones = relationship("Phone", cascade="all,delete-orphan")
    activities = relationship("Activity", secondary=org_activity, backref="organizations")
