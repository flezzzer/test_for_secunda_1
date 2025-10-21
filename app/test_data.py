from sqlalchemy.orm import Session
from app.core.db import SessionLocal, Base, engine
from app.models import Building, Activity, Organization
from app.services.organizations import create_organization
from app.services.buildings import create_building
from app.services.activities import create_activity
from app.core.config import settings

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_data(db: Session):
    buildings = {
        "Москва": db.query(Building).filter_by(address="г. Москва, ул. Ленина 1").first(),
        "СПБ": db.query(Building).filter_by(address="г. Санкт-Петербург, Невский проспект 50").first(),
    }

    if not buildings["Москва"]:
        buildings["Москва"] = create_building(db, "г. Москва, ул. Ленина 1", 55.751244, 37.618423)
    if not buildings["СПБ"]:
        buildings["СПБ"] = create_building(db, "г. Санкт-Петербург, Невский проспект 50", 59.9342802, 30.3350986)

    def get_or_create_activity(name, parent=None):
        act = db.query(Activity).filter_by(name=name).first()
        if act:
            return act
        return create_activity(db, name, parent.id if parent else None, settings.MAX_ACTIVITY_DEPTH)

    food = get_or_create_activity("Еда")
    meat = get_or_create_activity("Мясная продукция", food)
    dairy = get_or_create_activity("Молочная продукция", food)
    bakery = get_or_create_activity("Выпечка", food)
    cars = get_or_create_activity("Автомобили")
    trucks = get_or_create_activity("Грузовые", cars)
    light = get_or_create_activity("Легковые", cars)
    parts = get_or_create_activity("Запчасти", light)
    accessories = get_or_create_activity("Аксессуары", light)

    orgs = [
        {
            "name": "ООО Рога и Копыта",
            "building": buildings["Москва"].id,
            "phones": ["8-123-45-67", "8-111-22-33"],
            "activities": [meat.id, dairy.id],
        },
        {
            "name": "АО МясоСнаб",
            "building": buildings["СПБ"].id,
            "phones": ["8-987-65-43"],
            "activities": [meat.id],
        },
        {
            "name": "Пекарня Пряник",
            "building": buildings["Москва"].id,
            "phones": ["8-555-66-77"],
            "activities": [bakery.id],
        },
        {
            "name": "АвтоМир",
            "building": buildings["СПБ"].id,
            "phones": ["8-999-88-77"],
            "activities": [trucks.id, parts.id, accessories.id],
        },
    ]

    for o in orgs:
        exists = db.query(Organization).filter_by(name=o["name"]).first()
        if not exists:
            create_organization(db, o["name"], o["building"], o["phones"], o["activities"])

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        seed_data(db)
        print("Test data loaded successfully.")
    finally:
        db.close()
