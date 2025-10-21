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

    Args:
        o (OrganizationCreate): Данные организации (название, здание, телефоны, виды деятельности).
        db (Session, optional): Сессия базы данных.

    Returns:
        Organization: Созданная организация с ID и всеми связями.
    """
    return organizations.create_organization(db, o.name, o.building_id, o.phone_numbers, o.activity_ids)


@router.get("/by-building/{building_id}", response_model=List[Organization])
def by_building(building_id: int, db: Session = Depends(get_db)):
    """
    Возвращает список организаций, расположенных в конкретном здании.

    Args:
        building_id (int): ID здания.
        db (Session, optional): Сессия базы данных.

    Returns:
        List[Organization]: Организации, находящиеся в этом здании.
    """
    return organizations.get_orgs_by_building(db, building_id)


@router.get("/by-activity/{activity_id}", response_model=List[Organization])
def by_activity(activity_id: int, include_descendants: bool = True, db: Session = Depends(get_db)):
    """
    Возвращает список организаций по виду деятельности.

    Можно включить подвиды активности (include_descendants=True), чтобы получить все организации,
    которые занимаются этой деятельностью или её подкатегориями.

    Args:
        activity_id (int): ID активности.
        include_descendants (bool, optional): Включать подвиды активности. По умолчанию True.
        db (Session, optional): Сессия базы данных.

    Returns:
        List[Organization]: Организации с указанной активностью и её подкатегориями.
    """
    return organizations.get_orgs_by_activity(db, activity_id, include_descendants, settings.MAX_ACTIVITY_DEPTH)


@router.get("/search", response_model=List[Organization])
def search(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Поиск организаций по названию.

    Если name не указан, возвращается пустой список.

    Args:
        name (str, optional): Часть названия организации.
        db (Session, optional): Сессия базы данных.

    Returns:
        List[Organization]: Организации, которые содержат name в названии.
    """
    return organizations.search_by_name(db, name) if name else []


@router.get("/within-radius", response_model=List[Organization])
def within_radius(lat: float, lon: float, radius_km: float, db: Session = Depends(get_db)):
    """
    Находит организации в радиусе от заданной точки.

    Используется для отображения организаций на карте.

    Args:
        lat (float): Широта центра.
        lon (float): Долгота центра.
        radius_km (float): Радиус в километрах.
        db (Session, optional): Сессия базы данных.

    Returns:
        List[Organization]: Организации, находящиеся в заданном радиусе.
    """
    return organizations.orgs_within_radius(db, lat, lon, radius_km)


@router.get("/within-bbox", response_model=List[Organization])
def within_bbox(lat_min: float, lon_min: float, lat_max: float, lon_max: float, db: Session = Depends(get_db)):
    """
    Находит организации внутри прямоугольной области (bounding box).

    Args:
        lat_min (float): Минимальная широта.
        lon_min (float): Минимальная долгота.
        lat_max (float): Максимальная широта.
        lon_max (float): Максимальная долгота.
        db (Session, optional): Сессия базы данных.

    Returns:
        List[Organization]: Организации, находящиеся внутри bounding box.
    """
    return organizations.orgs_within_bbox(db, lat_min, lon_min, lat_max, lon_max)



@router.get("/{org_id}", response_model=Organization)
def get_org(org_id: int, db: Session = Depends(get_db)):
    """
    Получает организацию по её ID.

    Args:
        org_id (int): ID организации.
        db (Session, optional): Сессия базы данных.

    Returns:
        Organization: Организация с указанным ID.

    Raises:
        HTTPException: Если организация не найдена.
    """
    org = organizations.get_org_by_id(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Not found")
    return org

