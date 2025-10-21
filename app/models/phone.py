from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.db import Base

class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
