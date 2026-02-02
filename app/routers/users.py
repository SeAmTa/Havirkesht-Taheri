from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_
import math
import jdatetime

from ..db import get_db
from ..models import User, Role
from ..schemas import UserCreateAdminIn, UserSwaggerOut, UserUpdateSwaggerIn, UsersListOut
from ..security import require_auth, require_admin, hash_password


router = APIRouter(prefix="/users", tags=["Users"])


def to_jalali(dt):
    if not dt:
        return None
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime("%Y/%m/%d %H:%M:%S")


@router.post("/admin/", status_code=status.HTTP_201_CREATED, response_model=str, dependencies=[Depends(require_admin)])
def admin_create_user(payload: UserCreateAdminIn, db: Session = Depends(get_db)):
    # role_id معتبر؟
    role = db.query(Role).filter(Role.id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="role_id is invalid")

    # username تکراری نباشه
    exists = db.query(User).filter(User.username == payload.username).first()
    if exists:
        raise HTTPException(status_code=409, detail="username already exists")

    user = User(
        username=payload.username,
        password=hash_password(payload.password),
        fullname=payload.fullName,   # تبدیل fullName -> fullname
        email=payload.email,
        phone_number=payload.phone_number,
        disabled=bool(payload.disabled),
        role_id=payload.role_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Swagger گفته خروجی "string"؛ پس پیام ساده می‌دیم
    return "User created successfully"


@router.get("/{user_id}", response_model=UserSwaggerOut, dependencies=[Depends(require_auth)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSwaggerOut(
        created_at=user.created_at,
        created_at_jalali=to_jalali(user.created_at),
        updated_at=user.updated_at,
        updated_at_jalali=to_jalali(user.updated_at),
        id=user.id,
        username=user.username,
        email=user.email,
        fullname=user.fullname,
        phone_number=user.phone_number,
        role_id=user.role_id,
        disabled=bool(user.disabled),
    )


@router.put("/{user_id}", response_model=UserSwaggerOut, dependencies=[Depends(require_admin)])
def update_user(user_id: int, payload: UserUpdateSwaggerIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = db.query(Role).filter(Role.id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="role_id is invalid")

    user.username = payload.username
    user.password = hash_password(payload.password)
    user.fullname = payload.fullname
    user.email = payload.email
    user.phone_number = payload.phone_number
    user.role_id = payload.role_id
    user.disabled = bool(payload.disabled)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="username already exists")

    db.refresh(user)

    return UserSwaggerOut(
        created_at=user.created_at,
        created_at_jalali=to_jalali(user.created_at),
        updated_at=user.updated_at,
        updated_at_jalali=to_jalali(user.updated_at),
        id=user.id,
        username=user.username,
        email=user.email,
        fullname=user.fullname,
        phone_number=user.phone_number,
        role_id=user.role_id,
        disabled=bool(user.disabled),
    )


@router.get("/", response_model=UsersListOut, dependencies=[Depends(require_auth)])
def get_all_users(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    sort_by: str | None = Query(None),
    sort_order: str | None = Query(None, pattern="^(asc|desc)$"),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
):
    def to_jalali(dt):
        if not dt:
            return None
        return jdatetime.datetime.fromgregorian(datetime=dt).strftime("%Y/%m/%d %H:%M:%S")

    # --- فیلتر search ---
    filters = []
    if search:
        like = f"%{search}%"
        filters.append(
            or_(
                User.username.ilike(like),
                User.fullname.ilike(like),
                User.email.ilike(like),
                User.phone_number.ilike(like),
            )
        )

    base_query = db.query(User)
    if filters:
        base_query = base_query.filter(*filters)

    # --- sort ---
    allowed_sort = {
        "id": User.id,
        "username": User.username,
        "email": User.email,
        "fullname": User.fullname,
        "phone_number": User.phone_number,
        "role_id": User.role_id,
        "disabled": User.disabled,
        "created_at": User.created_at,
        "updated_at": User.updated_at,
    }

    if sort_by:
        if sort_by not in allowed_sort:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sort_by. Allowed: {', '.join(allowed_sort.keys())}",
            )
        col = allowed_sort[sort_by]
    else:
        col = User.id  # پیش‌فرض

    if (sort_order or "asc") == "desc":
        base_query = base_query.order_by(col.desc())
    else:
        base_query = base_query.order_by(col.asc())

    # --- pagination ---
    total = base_query.with_entities(func.count(User.id)).scalar() or 0
    pages = math.ceil(total / size) if total else 0
    offset = (page - 1) * size

    users = base_query.offset(offset).limit(size).all()

    items = [
        UserSwaggerOut(
            created_at=u.created_at,
            created_at_jalali=to_jalali(u.created_at),
            updated_at=u.updated_at,
            updated_at_jalali=to_jalali(u.updated_at),
            id=u.id,
            username=u.username,
            email=u.email,
            fullname=u.fullname,
            phone_number=u.phone_number,
            role_id=u.role_id,
            disabled=bool(u.disabled),
        )
        for u in users
    ]

    return UsersListOut(total=total, size=size, pages=pages, items=items)
