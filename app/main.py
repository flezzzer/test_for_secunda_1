from fastapi import FastAPI
from app.api.v1 import buildings, activities, organizations

app = FastAPI(title="Organizations Catalog API", version="1.0")

app.include_router(buildings.router, prefix="/api/v1/buildings", tags=["Buildings"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["Activities"])
app.include_router(organizations.router, prefix="/api/v1/organizations", tags=["Organizations"])
