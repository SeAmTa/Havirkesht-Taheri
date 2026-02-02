from math import ceil

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from ..db import get_db
from .. import models, schemas
from ..security import require_auth  # اگر خواستی فقط ادمین باشه: require_admin

router = APIRouter(tags=["Province"])


@router.post(
    "/province/",
    response_model=schemas.ProvinceCreatedOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_auth)],
)
def create_province(payload: schemas.ProvinceCreateIn, db: Session = Depends(get_db)):
    name = (payload.province or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="province is required")

    exists = db.query(models.Province).filter(models.Province.province == name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Province already exists")

    row = models.Province(province=name)
    db.add(row)
    db.commit()
    db.refresh(row)

    # طبق Swagger فقط province برمی‌گردونیم
    return {"province": row.province}


@router.get(
    "/province/",
    response_model=schemas.ProvinceListOut,
    dependencies=[Depends(require_auth)],
)
def get_all_provinces(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    sort_by: str | None = Query(None, description="Sort field"),
    sort_order: str | None = Query(None, pattern="^(asc|desc)$", description="Sort order"),
    search: str | None = Query(None, description="Search term"),
    db: Session = Depends(get_db),
):
    q = db.query(models.Province)

    if search:
        s = search.strip()
        if s:
            q = q.filter(models.Province.province.ilike(f"%{s}%"))

    total = q.count()

    # sort mapping (فقط فیلدهای مجاز)
    sort_map = {
        "id": models.Province.id,
        "province": models.Province.province,
        "created_at": models.Province.created_at,
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
        # پیش‌فرض: جدیدترین‌ها اول
        q = q.order_by(desc(models.Province.id))

    offset = (page - 1) * size
    rows = q.offset(offset).limit(size).all()

    pages = ceil(total / size) if total else 0

    items = [
        {
            "id": r.id,
            "province": r.province,
            "created_at": r.created_at,
        }
        for r in rows
    ]

    return {"total": total, "size": size, "pages": pages, "items": items}


@router.delete(
    "/province/{province}",
    response_model=schemas.MessageOut,
    dependencies=[Depends(require_auth)],
)
def delete_province(
    province: str,
    db: Session = Depends(get_db),
):
    name = (province or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="province is required")

    row = db.query(models.Province).filter(models.Province.province == name).first()
    if not row:
        raise HTTPException(status_code=404, detail="Province not found")

    db.delete(row)
    db.commit()

    return {"message": "Province deleted successfully"}
