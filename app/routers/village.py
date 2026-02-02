from math import ceil

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from ..db import get_db
from .. import models, schemas
from ..security import require_auth

router = APIRouter(tags=["Village"])


@router.post(
    "/village/",
    response_model=schemas.VillageCreatedOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_auth)],
)
def create_village(payload: schemas.VillageCreateIn, db: Session = Depends(get_db)):
    name = (payload.village or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="village is required")

    city = db.query(models.City).filter(models.City.id == payload.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    exists = db.query(models.Village).filter(models.Village.village == name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Village already exists")

    row = models.Village(village=name, city_id=payload.city_id)
    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "village": row.village,
        "city_id": row.city_id,
        "id": row.id,
        "created_at": row.created_at,
        "city": city.city,
    }


@router.get(
    "/village/",
    response_model=schemas.VillageListOut,
    dependencies=[Depends(require_auth)],
)
def get_all_villages(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    sort_by: str | None = Query(None, description="Sort field"),
    sort_order: str | None = Query(None, pattern="^(asc|desc)$", description="Sort order"),
    search: str | None = Query(None, description="Search term"),
    city_id: int | None = Query(None, description="Filter by city ID"),
    db: Session = Depends(get_db),
):
    # join برای اینکه city name برگرده
    q = db.query(models.Village, models.City).join(models.City, models.Village.city_id == models.City.id)

    if city_id is not None:
        q = q.filter(models.Village.city_id == city_id)

    if search:
        s = search.strip()
        if s:
            q = q.filter(models.Village.village.ilike(f"%{s}%"))

    total = q.count()

    # sort fields مجاز
    sort_map = {
        "id": models.Village.id,
        "village": models.Village.village,
        "city_id": models.Village.city_id,
        "created_at": models.Village.created_at,
        "city": models.City.city,  # این یکی هم از روی join
    }

    if sort_by:
        col = sort_map.get(sort_by)
        if not col:
            raise HTTPException(status_code=400, detail="Invalid sort_by")
        q = q.order_by(desc(col) if sort_order == "desc" else asc(col))
    else:
        q = q.order_by(desc(models.Village.id))

    rows = q.offset((page - 1) * size).limit(size).all()
    pages = ceil(total / size) if total else 0

    items = []
    for v, c in rows:
        items.append(
            {
                "village": v.village,
                "city_id": v.city_id,
                "id": v.id,
                "created_at": v.created_at,
                "city": c.city,
            }
        )

    return {"total": total, "size": size, "pages": pages, "items": items}


@router.delete(
    "/village/{village}",
    response_model=schemas.MessageOut,
    dependencies=[Depends(require_auth)],
)
def delete_village(
    village: str = Path(..., description="village"),
    db: Session = Depends(get_db),
):
    name = (village or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="village is required")

    row = db.query(models.Village).filter(models.Village.village == name).first()
    if not row:
        raise HTTPException(status_code=404, detail="Village not found")

    db.delete(row)
    db.commit()
    return {"message": "Village deleted successfully"}
