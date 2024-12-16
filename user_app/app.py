# Файл app.py связывает маршруты (эндпоинты) с логикой из crud.py, схемами из schemas.py и сессией базы данных из database.py.

from fastapi import APIRouter
from . import crud, schemas, models
from database import SessionLocal

user_app_router = APIRouter()  # Создаётся экземпляр APIRouter, который будет хранить маршруты, связанные с пользователями.


#  Маршрут для создания пользователя
@user_app_router.post("/users/", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate):
    db = SessionLocal()   # # Создаём сессию базы данных
    return crud.create_user(db=db, user=user)  # # Вызываем функцию из crud.py

@user_app_router.get("/users/", response_model=list[schemas.UserInfo])
def get_users():
    db = SessionLocal()
    return crud.get_all_users(db)


@user_app_router.put("/user/{user_id}/", response_model=schemas.UserInfo)
def update_user(user_id: int, user: schemas.UserCreate):
    db = SessionLocal()
    return crud.update_user(db=db,user_id=user_id,user=user)

@user_app_router.delete("/user/{user_id}/")
def delete_user(user_id : int):
    db = SessionLocal()
    return crud.delete_user(db=db,user_id=user_id)



# APIRouter - Это специальный объект в FastAPI,
# который помогает группировать маршруты (эндпоинты).
# Вместо того чтобы добавлять маршруты напрямую в app, мы используем APIRouter, чтобы структурировать код.

# Маршрут для создания пользователя (POST /users/).
# Маршрут для получения списка всех пользователей (GET /users/).
# Оба маршрута используют сессию базы данных и функции из модуля crud для взаимодействия с базой данных.
# Данные проходят валидацию и сериализацию с помощью Pydantic-схем из модуля schemas.