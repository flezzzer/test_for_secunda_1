from sqlalchemy.orm import Session
from app.models.building import Building

def create_building(db: Session, address: str, latitude: float, longitude: float):
    b = Building(address=address, latitude=latitude, longitude=longitude)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b

def get_buildings(db: Session):
    return db.query(Building).all()
