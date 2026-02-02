from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------- Users ----------

class UserCreateAdminIn(BaseModel):
    username: str
    password: str
    fullName: str
    email: str
    disabled: bool = False
    role_id: int
    phone_number: str


class UserSwaggerOut(BaseModel):
    created_at: Optional[datetime] = None
    created_at_jalali: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_at_jalali: Optional[str] = None

    id: int
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    phone_number: Optional[str] = None
    role_id: int
    disabled: bool


class UserUpdateSwaggerIn(BaseModel):
    username: str
    password: str
    fullname: str
    email: str
    phone_number: str
    role_id: int
    disabled: bool


class UsersListOut(BaseModel):
    total: int
    size: int
    pages: int
    items: List[UserSwaggerOut]


# ---------- Auth ----------

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# ---------- Province ----------

class ProvinceCreateIn(BaseModel):
    province: str


# خروجی POST طبق Swagger (فقط province)
class ProvinceCreatedOut(BaseModel):
    province: str


# آیتم‌های لیست GET (طبق Swagger: id, province, created_at)
class ProvinceOut(BaseModel):
    id: int
    province: str
    created_at: Optional[datetime] = None


class ProvinceListOut(BaseModel):
    total: int
    size: int
    pages: int
    items: List[ProvinceOut]


# خروجی DELETE طبق Swagger
class MessageOut(BaseModel):
    message: str


# ---------- City ----------

class CityCreateIn(BaseModel):
    city: str
    province_id: int


class CityCreatedOut(BaseModel):
    city: str
    province_id: int
    id: int
    created_at: Optional[datetime] = None


class CityOut(BaseModel):
    city: str
    province_id: int
    id: int
    created_at: Optional[datetime] = None


class CityListOut(BaseModel):
    total: int
    size: int
    pages: int
    items: List[CityOut]


class MessageOut(BaseModel):
    message: str


# ---------- Village ----------

class VillageCreateIn(BaseModel):
    village: str
    city_id: int

class VillageCreatedOut(BaseModel):
    village: str
    city_id: int
    id: int
    created_at: Optional[datetime] = None
    city: str

class VillageOut(BaseModel):
    village: str
    city_id: int
    id: int
    created_at: Optional[datetime] = None
    city: str

class VillageListOut(BaseModel):
    total: int
    size: int
    pages: int
    items: List[VillageOut]


# ---------- CropYear ----------

class CropYearCreateIn(BaseModel):
    crop_year_name: str

class CropYearCreatedOut(BaseModel):
    crop_year_name: str
    id: int
    created_at: Optional[datetime] = None

class CropYearOut(BaseModel):
    id: int
    crop_year_name: str
    created_at: Optional[datetime] = None

class CropYearListOut(BaseModel):
    total: int
    size: int
    pages: int
    items: List[CropYearOut]



# ---------- Farmer ----------

class FarmerCreateIn(BaseModel):
    national_id: str
    full_name: str
    father_name: str
    phone_number: str
    sheba_number_1: str
    sheba_number_2: str
    card_number: str
    address: str

class FarmerOut(BaseModel):
    national_id: str
    full_name: str
    father_name: str
    phone_number: str
    sheba_number_1: str
    sheba_number_2: str
    card_number: str
    address: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class FarmerListOut(BaseModel):
    total: int
    size: int
    pages: int
    items: list[FarmerOut]