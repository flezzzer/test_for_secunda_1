from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Organization, Activity, Building, Phone
from app.services.activities import get_activity_descendants
import math

def create_organization(db: Session, name: str, building_id: int, phones: list[str], activity_ids: list[int]):
    org = Organization(name=name, building_id=building_id)
    db.add(org)
    db.flush()
    for num in phones:
        db.add(Phone(number=num, organization_id=org.id))
    if activity_ids:
        acts = db.execute(select(Activity).where(Activity.id.in_(activity_ids))).scalars().all()
        org.activities = acts
    db.commit()
    db.refresh(org)
    return org

def get_org_by_id(db: Session, org_id: int):
    return db.get(Organization, org_id)

def get_orgs_by_building(db: Session, building_id: int):
    return db.execute(select(Organization).where(Organization.building_id == building_id)).scalars().all()

def get_orgs_by_activity(db: Session, activity_id: int, include_descendants: bool, max_depth: int):
    if include_descendants:
        ids = get_activity_descendants(db, activity_id, max_depth)
    else:
        ids = {activity_id}
    stmt = select(Organization).join(Organization.activities).where(Activity.id.in_(ids)).distinct()
    return db.execute(stmt).scalars().all()

def search_by_name(db: Session, name: str):
    return db.execute(select(Organization).where(Organization.name.ilike(f"%{name}%"))).scalars().all()

# гео-функции (P.S. путем гуглинга решил, что формула гаверсинуса лучше всего подходит)
def haversine(lon1, lat1, lon2, lat2):
    from math import radians, sin, cos, asin, sqrt
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    R = 6371 # радиус земли в км
    return R * c

def orgs_within_radius(db: Session, lat: float, lon: float, radius_km: float):
    R = 6371
    max_lat = lat + (radius_km / R) * (180 / math.pi)
    min_lat = lat - (radius_km / R) * (180 / math.pi)
    max_lon = lon + (radius_km / R) * (180 / math.pi) / math.cos(lat * math.pi / 180)
    min_lon = lon - (radius_km / R) * (180 / math.pi) / math.cos(lat * math.pi / 180)
    stmt = select(Organization, Building).join(Building).where(
        Building.latitude.between(min_lat, max_lat),
        Building.longitude.between(min_lon, max_lon),
    )
    results = []
    for org, b in db.execute(stmt):
        if haversine(lon, lat, b.longitude, b.latitude) <= radius_km:
            results.append(org)
    return results

def orgs_within_bbox(db: Session, lat_min, lon_min, lat_max, lon_max):
    stmt = select(Organization).join(Building).where(
        Building.latitude.between(lat_min, lat_max),
        Building.longitude.between(lon_min, lon_max),
    )
    return db.execute(stmt).scalars().all()
