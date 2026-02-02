from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
from app.db import get_db
from app import models, schemas
from app.security import require_auth

router = APIRouter(tags=["Farmer"])

# ایجاد فارمر
@router.post("/farmer/", response_model=schemas.FarmerOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_auth)],)
def create_farmer(payload: schemas.FarmerCreateIn, db: Session = Depends(get_db)):
    # بررسی وجود فارمر با همان شناسه ملی
    exists = db.query(models.Farmer).filter(models.Farmer.national_id == payload.national_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Farmer with this national_id already exists")
    
    # اضافه کردن فارمر جدید
    farmer = models.Farmer(**payload.dict())
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    
    return farmer

# دریافت همه فارمرها
@router.get("/farmer/", response_model=schemas.FarmerListOut, dependencies=[Depends(require_auth)],)
def get_all_farmers(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search by name or national id"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Farmer)

    if search:
        query = query.filter(models.Farmer.full_name.ilike(f"%{search}%") | models.Farmer.national_id.ilike(f"%{search}%"))
    
    total = query.count()
    offset = (page - 1) * size
    rows = query.offset(offset).limit(size).all()

    pages = (total + size - 1) // size  # محاسبه تعداد صفحات

    return {"total": total, "size": size, "pages": pages, "items": rows}

# دریافت فارمر بر اساس شناسه ملی
@router.get("/farmer/{national_id}", response_model=schemas.FarmerOut, dependencies=[Depends(require_auth)],)
def get_farmer_by_national_id(national_id: str, db: Session = Depends(get_db)):
    farmer = db.query(models.Farmer).filter(models.Farmer.national_id == national_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer

# به‌روزرسانی فارمر
@router.put("/farmer/{national_id}", response_model=schemas.FarmerOut, dependencies=[Depends(require_auth)],)
def update_farmer(national_id: str, payload: schemas.FarmerCreateIn, db: Session = Depends(get_db)):
    farmer = db.query(models.Farmer).filter(models.Farmer.national_id == national_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    for key, value in payload.dict().items():
        setattr(farmer, key, value)
    
    db.commit()
    db.refresh(farmer)
    return farmer

# حذف فارمر
@router.delete("/farmer/{national_id}", dependencies=[Depends(require_auth)],)
def delete_farmer(national_id: str, db: Session = Depends(get_db)):
    farmer = db.query(models.Farmer).filter(models.Farmer.national_id == national_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    db.delete(farmer)
    db.commit()
    return {"message": "Farmer deleted successfully"}

# دریافت شناسه کاربری بر اساس شناسه ملی
@router.get("/farmer/farmer-id-to-user-id/{farmer_id}", )
def get_user_id_from_farmer_id(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.query(models.Farmer).filter(models.Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    # فرض بر این است که فارمر دارای یک شناسه کاربری باشد (در اینجا فقط برای نمایش فرضی است)
    user_id = farmer.id  # می‌توانید از طریق روابط مدل خود به user_id دسترسی داشته باشید
    return {"user_id": user_id}
