from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.schemas.organization import Organization, OrganizationCreate
from app.services import organizations
from app.core.deps import get_db, require_api_key
from app.core.config import settings
from typing import List, Optional

router = APIRouter(dependencies=[Depends(require_api_key)])

@router.post("/", response_model=Organization)
def create_org(o: OrganizationCreate, db: Session = Depends(get_db)):
    """
    Создаёт новую организацию.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.

    **Body**:
    - **name (str)**: Название организации
    - **building_id (int)**: ID здания, к которому привязана организация
    - **phone_numbers (List[str])**: Список номеров телефонов организации
    - **activity_ids (List[int])**: Список ID активностей организации


    **Returns**:
    - **Orrganization**: Созданное здание с его ID.
    """
    return organizations.create_organization(db, o.name, o.building_id, o.phone_numbers, o.activity_ids)


@router.get("/by-building/{building_id}", response_model=List[Organization])
def by_building(building_id: int, db: Session = Depends(get_db)):
    """
    Возвращает список организаций, расположенных в конкретном здании.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.
    - **building_id (int)**: ID здания

    **Returns**:
     - **List[Organization]**: Список организаций.
    """
    return organizations.get_orgs_by_building(db, building_id)


@router.get("/by-activity/{activity_id}", response_model=List[Organization])
def by_activity(activity_id: int, include_descendants: bool = True, db: Session = Depends(get_db)):
    """
    Возвращает список организаций по виду деятельности.

    Можно включить подвиды активности (include_descendants=True), чтобы получить все организации,
    которые занимаются этой деятельностью или её подкатегориями.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.
    - **activity_id (int)**: ID активности
    - **include_descendants (bool, optional)**: Включать ли возможность поиска подкатегорий активности

    **Returns**:
     - **List[Organization]**: Список организаций.
    """
    return organizations.get_orgs_by_activity(db, activity_id, include_descendants, settings.MAX_ACTIVITY_DEPTH)


@router.get("/search", response_model=List[Organization])
def search(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Поиск организаций по названию.

    Если name не указан, возвращается пустой список.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.
    - **name (str)**: Название организации

    **Returns**:
     - **List[Organization]**: Список организаций.
    """
    return organizations.search_by_name(db, name) if name else []


@router.get("/within-radius", response_model=List[Organization])
def within_radius(lat: float, lon: float, radius_km: float, db: Session = Depends(get_db)):
    """
    Находит организации в радиусе от заданной точки.

    Используется для отображения организаций на карте.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.
    - **lat (float)**: Широта центра
    - **lon (float)**: Долгота центра
    - **radius_km (float)**: Радиус в км. от центра

    **Returns**:
     - **List[Organization]**: Список организаций.
    """
    return organizations.orgs_within_radius(db, lat, lon, radius_km)


@router.get("/within-bbox", response_model=List[Organization])
def within_bbox(lat_min: float, lon_min: float, lat_max: float, lon_max: float, db: Session = Depends(get_db)):
    """
    Находит организации внутри прямоугольной области (bounding box).

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.
    - **lat_min (float)**: Минимальная широта.
    - **lon_min (float)**: Минимальная долгота.
    - **lat_max (float)**: Максимальная широта.
    - **lon_max (float)** Максимальная долгота.

    **Returns**:
     - **List[Organization]**: Список организаций.
    """
    return organizations.orgs_within_bbox(db, lat_min, lon_min, lat_max, lon_max)



@router.get("/{org_id}", response_model=Organization)
def get_org(org_id: int, db: Session = Depends(get_db)):
    """
    Получает организацию по её ID.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.
    - **org_id (int)**: ID организации

    **Returns**:
     - **Organization**: Найденная организация.

    **Raises**:
    - **HTTPException**: Если организация не найдена.
    """
    org = organizations.get_org_by_id(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Not found")
    return org

