from math import ceil

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from sqlalchemy.exc import IntegrityError

from ..db import get_db
from .. import models, schemas
from ..security import require_auth  # اگر خواستی فقط ادمین باشه: require_admin

router = APIRouter(tags=["City"])


@router.post(
    "/city/",
    response_model=schemas.CityCreatedOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_auth)],
)
def create_city(payload: schemas.CityCreateIn, db: Session = Depends(get_db)):
    name = (payload.city or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="city is required")

    # province باید وجود داشته باشد
    prov = db.query(models.Province).filter(models.Province.id == payload.province_id).first()
    if not prov:
        raise HTTPException(status_code=404, detail="Province not found")

    # unique city
    exists = db.query(models.City).filter(models.City.city == name).first()
    if exists:
        raise HTTPException(status_code=409, detail="City already exists")

    row = models.City(city=name, province_id=payload.province_id)
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="City already exists")

    db.refresh(row)
    return {"city": row.city, "province_id": row.province_id, "id": row.id, "created_at": row.created_at}


@router.get(
    "/city/",
    response_model=schemas.CityListOut,
    dependencies=[Depends(require_auth)],
)
def get_all_cities(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    sort_by: str | None = Query(None, description="Sort field"),
    sort_order: str | None = Query(None, pattern="^(asc|desc)$", description="Sort order"),
    search: str | None = Query(None, description="Search term"),
    province_id: int | None = Query(None, description="Filter by province ID"),
    db: Session = Depends(get_db),
):
    q = db.query(models.City)

    if province_id is not None:
        q = q.filter(models.City.province_id == province_id)

    if search:
        s = search.strip()
        if s:
            q = q.filter(models.City.city.ilike(f"%{s}%"))

    total = q.count()

    sort_map = {
        "id": models.City.id,
        "city": models.City.city,
        "province_id": models.City.province_id,
        "created_at": models.City.created_at,
    }

    if sort_by:
        col = sort_map.get(sort_by)
        if not col:
            raise HTTPException(status_code=400, detail="Invalid sort_by")
        if sort_order == "desc":
            q = q.order_by(desc(col))
        else:
            q = q.order_by(asc(col))
    else:
        q = q.order_by(desc(models.City.id))

    offset = (page - 1) * size
    rows = q.offset(offset).limit(size).all()

    pages = ceil(total / size) if total else 0

    items = [
        {"city": r.city, "province_id": r.province_id, "id": r.id, "created_at": r.created_at}
        for r in rows
    ]
    return {"total": total, "size": size, "pages": pages, "items": items}


@router.delete(
    "/city/{city}",
    response_model=schemas.MessageOut,
    dependencies=[Depends(require_auth)],
)
def delete_city(city: str, db: Session = Depends(get_db)):
    name = (city or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="city is required")

    row = db.query(models.City).filter(models.City.city == name).first()
    if not row:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # مثلا اگر Village بهش FK داشته باشه
        raise HTTPException(status_code=409, detail="City cannot be deleted (it is referenced)")

    return {"message": "City deleted successfully"}
