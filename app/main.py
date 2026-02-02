from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers.users import router as users_router
from .routers.auth import router as auth_router
from .routers.province import router as province_router
from .routers.city import router as city_router
from .routers.village import router as village_router
from .routers import crop_year
from app.routers import farmer

app = FastAPI(title="Havirkesht API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    #["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # مجاز بودن این متدها
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(province_router)
app.include_router(city_router)
app.include_router(village_router)
app.include_router(crop_year.router)
app.include_router(farmer.router)
