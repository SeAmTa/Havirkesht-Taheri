from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from math import ceil

from ..db import get_db
from .. import models, schemas
from ..security import require_auth  # در صورت نیاز به ادمین

router = APIRouter(tags=["Crop Year"])

@router.post(
    "/crop-year/",
    response_model=schemas.CropYearCreatedOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_auth)],
)
def create_crop_year(payload: schemas.CropYearCreateIn, db: Session = Depends(get_db)):
    crop_year_name = payload.crop_year_name.strip()
    if not crop_year_name:
        raise HTTPException(status_code=400, detail="Crop year name is required")

    exists = db.query(models.CropYear).filter(models.CropYear.crop_year_name == crop_year_name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Crop year already exists")

    row = models.CropYear(crop_year_name=crop_year_name)
    db.add(row)
    db.commit()
    db.refresh(row)

    return {"crop_year_name": row.crop_year_name, "id": row.id, "created_at": row.created_at}


@router.get(
    "/crop-year/",
    response_model=schemas.CropYearListOut,
    dependencies=[Depends(require_auth)],
)
def get_all_crop_years(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    search: str | None = Query(None, description="Search term"),
    db: Session = Depends(get_db),
):
    q = db.query(models.CropYear)

    if search:
        s = search.strip()
        if s:
            q = q.filter(models.CropYear.crop_year_name.ilike(f"%{s}%"))

    total = q.count()

    rows = q.offset((page - 1) * size).limit(size).all()

    pages = ceil(total / size) if total else 0

    items = [
        {
            "id": r.id,
            "crop_year_name": r.crop_year_name,
            "created_at": r.created_at,
        }
        for r in rows
    ]

    return {"total": total, "size": size, "pages": pages, "items": items}


@router.delete(
    "/crop-year/{crop_year_name}",
    response_model=schemas.MessageOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_auth)],
)
def delete_crop_year(crop_year_name: str, db: Session = Depends(get_db)):
    row = db.query(models.CropYear).filter(models.CropYear.crop_year_name == crop_year_name).first()

    if not row:
        raise HTTPException(status_code=404, detail="Crop year not found")

    db.delete(row)
    db.commit()

    return {"message": f"Crop year {crop_year_name} deleted successfully"}
