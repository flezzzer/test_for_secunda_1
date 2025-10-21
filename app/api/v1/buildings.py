from fastapi import APIRouter, Depends
from app.schemas.building import Building, BuildingCreate
from app.services import buildings
from app.core.deps import get_db, require_api_key
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(dependencies=[Depends(require_api_key)])

@router.post("/", response_model=Building)
def create_building_api(b: BuildingCreate, db: Session = Depends(get_db)):
    """
    Создаёт новое здание.

    Можно добавить адрес здания и его координаты (широта/долгота), чтобы привязывать организации к карте.

    Args:
        b (BuildingCreate): Данные здания (адрес, широта, долгота).
        db (Session, optional): Сессия базы данных.

    Returns:
        Building: Созданное здание с его ID.
    """
    return buildings.create_building(db, b.address, b.latitude, b.longitude)


@router.get("/", response_model=List[Building])
def list_buildings_api(db: Session = Depends(get_db)):
    """
    Возвращает список всех зданий.

    Используется для выбора здания при создании организации или для отображения на карте.

    Args:
        db (Session, optional): Сессия базы данных.

    Returns:
        List[Building]: Список всех зданий.
    """
    return buildings.get_buildings(db)

