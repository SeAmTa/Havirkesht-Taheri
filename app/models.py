from sqlalchemy import BigInteger, Integer, String, Boolean, TIMESTAMP, ForeignKey, DateTime, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base
from datetime import datetime


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String(255))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    fullname: Mapped[str | None] = mapped_column(String(255))
    phone_number: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(255))

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship("Role")

    created_at: Mapped[object | None] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    updated_at: Mapped[object | None] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    token = Column(String(255), nullable=False, unique=True)
    blacklisted_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Province(Base):
    __tablename__ = "province"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    province: Mapped[str | None] = mapped_column(String(255), unique=True)

    created_at: Mapped[object | None] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=True
    )
    updated_at: Mapped[object | None] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=True,
    )

class City(Base):
    __tablename__ = "city"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    city = Column(String(255), unique=True, nullable=False)

    province_id = Column(BigInteger, ForeignKey("province.id"), nullable=False)
    province = relationship("Province")

    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=True)
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=True)


class Village(Base):
    __tablename__ = "village"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    village = Column(String(255), nullable=False, unique=True)

    city_id = Column(BigInteger, ForeignKey("city.id"), nullable=False)
    city_rel = relationship("City")

    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=True)
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=True)


class CropYear(Base):
    __tablename__ = "crop_year"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    crop_year_name = Column(String(255), unique=True)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=True)


class Farmer(Base):
    __tablename__ = "farmer"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    national_id = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    father_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    sheba_number_1 = Column(String(26), nullable=False)
    sheba_number_2 = Column(String(26), nullable=False)
    card_number = Column(String(16), nullable=False)
    address = Column(String(255), nullable=False)

    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=True)
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=True,)