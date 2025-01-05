from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import FileResponse, HTMLResponse

import database
import os
from user_app import models, schemas, crud
import json
from loger_config import service_logger as logger
from user_app.app import user_app_router


# http://localhost:8001/  - используем этот адрес если другие не работают
# docker build -t fastapi-project .
# docker run -p 8001:8001 fastapi-project
# uvicorn main:app --reload
# uvicorn main:app --port 8001 --reload

app = FastAPI()

app.include_router(user_app_router, prefix="/user_app", tags=["users"])
IMAGE_PATH = os.path.join(os.getcwd(), "static", "example.jpg")




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


@app.get("/", response_class=HTMLResponse)
async def read_main():
    # HTML с картинкой
    # HTML с текстом поверх картинки
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
        <style>
            .image-container {{
                position: relative;
                text-align: center;
                color: white;
                font-family: Arial, sans-serif;
            }}
            .centered-text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 2em;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 0.5); /* Полупрозрачный фон для выделения текста */
                padding: 10px 20px;
                border-radius: 10px;
            }}
            .docs-link {{
                position: absolute;
                top: 60%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 1.2em;
                color: #ffffff;
                text-decoration: none;
                background-color: rgba(0, 0, 0, 0.5);
                padding: 8px 15px;
                border-radius: 5px;
            }}
            .docs-link:hover {{
                background-color: rgba(0, 0, 0, 0.8);
            }}
        </style>
    </head>
    <body>
        <h1>Welcome Page</h1>
        <div class="image-container">
            <img src="/image" alt="Example Image" style="max-width: 100%; height: auto;">
            <div class="centered-text">Hello User</div>
            <a href="/docs" target="_blank" class="docs-link">Перейти к документации FastAPI</a>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@app.get("/image")
async def get_image():
    if not os.path.exists(IMAGE_PATH):
        return {"error": "Image not found!"}
    return FileResponse(IMAGE_PATH)








