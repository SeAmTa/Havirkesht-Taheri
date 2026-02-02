# app/security.py
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from typing import Optional

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# auto_error=False یعنی اگر توکن نبود خودش 401 نده، ما خودمون تصمیم می‌گیریم
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)


# --------- PASSWORD HASHING ---------
def _ensure_bcrypt_limit(raw_password: str) -> None:
    # bcrypt حداکثر 72 بایت
    if len(raw_password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password is too long (bcrypt limit is 72 bytes). Use a shorter password.",
        )


def hash_password(raw: str) -> str:
    _ensure_bcrypt_limit(raw)
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)


# --------- JWT TOKEN CREATION ---------
def _create_token(*, subject: str, token_type: str, expires_delta: timedelta, secret: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,          # user_id
        "type": token_type,      # access | refresh
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, secret, algorithm=settings.JWT_ALG)


def create_access_token(user_id: int) -> str:
    return _create_token(
        subject=str(user_id),
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret=settings.JWT_SECRET,
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
        subject=str(user_id),
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        secret=settings.JWT_REFRESH_SECRET,
    )


# --------- TOKEN VALIDATION ---------
def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_REFRESH_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


# --------- BLACKLIST ---------
def is_blacklisted(db: Session, token: str) -> bool:
    return (
        db.query(models.TokenBlacklist)
        .filter(models.TokenBlacklist.token == token)
        .first()
        is not None
    )


def blacklist_token(db: Session, token: str) -> None:
    if not token:
        return
    if not is_blacklisted(db, token):
        db.add(models.TokenBlacklist(token=token))
        db.commit()


# --------- INTERNAL: get user from access token ---------
def _get_user_from_access_token(db: Session, token: str) -> models.User:
    if is_blacklisted(db, token):
        raise HTTPException(status_code=401, detail="Token is blacklisted")

    payload = decode_access_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid access token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if getattr(user, "disabled", False):
        raise HTTPException(status_code=403, detail="User is disabled")

    return user


# --------- REQUIRE AUTH / ADMIN ---------
def require_auth(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme),
) -> Optional[models.User]:
    # اگر Auth خاموش باشد، اصلاً توکن لازم نداریم
    if settings.DISABLE_AUTH == 1:
        return None

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return _get_user_from_access_token(db, token)


def require_admin(
    current_user: Optional[models.User] = Depends(require_auth),
) -> Optional[models.User]:
    if settings.DISABLE_AUTH == 1:
        return None

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # فعلاً فرض: role_id=1 یعنی admin
    if getattr(current_user, "role_id", None) != 1:
        raise HTTPException(status_code=403, detail="Admin only")

    return current_user
