# Этот файл содержит функции, которые взаимодействуют с базой данных (CRUD — Create, Read, Update, Delete).
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from user_app import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()





def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    try:
        db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        #return {"message": "User deleted successfully"}
        return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
