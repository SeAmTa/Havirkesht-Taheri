from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, schemas
from ..security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    blacklist_token,
    is_blacklisted,
    hash_password,
    require_auth,
)

router = APIRouter(tags=["Auth"])


@router.post("/token", response_model=schemas.TokenResponse)
def login_for_access_token(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == form.username).first()

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    if getattr(user, "disabled", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is disabled")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh-token", response_model=schemas.TokenResponse)
def refresh_access_token(
    refresh_token: str = Query(..., description="refresh_token"),
    db: Session = Depends(get_db),
):
    # مطابق Swagger: refresh_token در Query
    if is_blacklisted(db, refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is blacklisted")

    data = decode_refresh_token(refresh_token)
    if data.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = data.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if getattr(user, "disabled", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is disabled")

    # (اختیاری) می‌تونی رفرش قبلی رو بلاک کنی:
    # blacklist_token(db, refresh_token)

    new_access = create_access_token(user.id)
    new_refresh = create_refresh_token(user.id)

    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}


@router.post("/logout")
def logout(
    access_token: str | None = Query(default=None, description="access_token"),
    refresh_token: str | None = Query(default=None, description="refresh_token"),
    db: Session = Depends(get_db),
):
    # طبق Swagger هر کدوم می‌تونه باشه، ولی حداقل یکی لازمه
    if not access_token and not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="access_token or refresh_token is required",
        )

    if access_token:
        blacklist_token(db, access_token)
    if refresh_token:
        blacklist_token(db, refresh_token)

    return {"message": "Logged out successfully"}


@router.post("/changepassword/")
def change_password(
    payload: schemas.ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(require_auth),
):
    # اگر DISABLE_AUTH=1 باشد، current_user ممکن است None باشد
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not verify_password(payload.old_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    current_user.password = hash_password(payload.new_password)
    db.commit()

    return {"message": "Password changed successfully"}
