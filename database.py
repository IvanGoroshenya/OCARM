# # database.py для настройки базы данных:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # Настраивает соединение с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Создаёт сессии для выполнения SQL-запросов.
Base = declarative_base()  #  Базовый класс для всех моделей (таблиц), которые вы определяете в models.py.

# Создание таблиц
Base.metadata.create_all(bind=engine)

