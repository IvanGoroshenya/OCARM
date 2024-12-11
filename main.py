from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database, crud
import logging
import json
from loger_config import service_logger as logger



# uvicorn main:app --reload
# uvicorn main:app --port 8001 --reload

app = FastAPI()



@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host if request.client else "Unknown"
    logger.info(f"Request to {request.url} - Method: {request.method} - Client IP: {client_ip}")

    query_params = dict(request.query_params)
    if query_params:
        logger.debug(f"Query Params: {query_params}")

    body = await request.body()
    if body:
        try:
            parsed_body = json.loads(body.decode("utf-8"))
            logger.debug(f"Request Body: {json.dumps(parsed_body, indent=2)}")
        except json.JSONDecodeError:
            logger.debug(f"Request Body (raw): {body.decode('utf-8')}")

    response = await call_next(request)
    logger.info(f"Response: {response.status_code} for {request.method} {request.url}")
    return response






def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}







# @app.post("/users/", response_model=schemas.UserInfo)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

@app.post("/users/",response_model=schemas.UserInfo)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail="Invalid data")


@app.get("/users/", response_model=List[schemas.UserInfo])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserInfo)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.put("/users/{user_id}", response_model=schemas.UserInfo)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)


@app.delete("/users/{user_id}", response_model=schemas.UserInfo)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)



#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# list_of_usernames = []
#
# @app.get('/user/{user_name}')
# def write_user(user_name: str, user_id: int):
#     logger.info(f"Getting user: {user_name} with ID: {user_id}")
#
#     return {"Name": user_name, "User_id": user_id}
#
# @app.put('/user_name/{user_name}')
# def put_data(user_name: str):
#     logger.info(f"Adding username: {user_name}")
#     logger.debug(f"Adding username: {user_name}")
#     list_of_usernames.append(user_name)
#     return {"username": user_name}
#
# @app.post('/postData/')
# def post_data(user_name: str):
#     logger.info(f"Posting data for username: {user_name}")
#     list_of_usernames.append(user_name)
#     return {"username": list_of_usernames}
#
# @app.delete("/deleteData/{user_name}")
# def delete_data(user_name: str):
#     logger.info(f"Deleting username: {user_name}")
#     list_of_usernames.remove(user_name)
#     return {'usernames': list_of_usernames}