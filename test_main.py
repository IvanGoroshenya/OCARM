import starlette
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import database
from database import Base
from main import app, get_db
from models import User
import  time
from sqlalchemy import distinct
from main import app


# Создаем тестовую базу данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Переопределяем зависимость get_db для тестов
def override_get_db():
    print("Используется база данных:", SQLALCHEMY_DATABASE_URL)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Переопределяем зависимость в приложении
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_client():
    print(' База данных очищается')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print('База данных очищена')
    client = TestClient(app)
    yield client
    # Удаление таблиц после теста
    Base.metadata.drop_all(bind=engine)






# Настройте фиктуру для базы данных  def test_get_users(test_client, session): этот тест не проходил без этого
@pytest.fixture(scope="module")
def session():
    engine = create_engine("sqlite:///./test_test.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def test_client():

    with TestClient(app) as client:
        yield client






def test_create_user(test_client):           # pytest -k "test_create_user"   - проверка этой функции
    # Данные для нового пользователя
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    }

    # Отправка POST-запроса на создание пользователя
    response = test_client.post("/users/", json=user_data)

    # Проверяем, что запрос выполнен успешно
    assert response.status_code == 200

    # Проверяем, что возвращенные данные совпадают с переданными
    response_data = response.json()
    assert response_data["first_name"] == user_data["first_name"]
    assert response_data["last_name"] == user_data["last_name"]
    assert response_data["email"] == user_data["email"]
    assert "user_id" in response_data



# Тест для проверки получения пользователей
def test_get_users(test_client, session):
    # Очищаем базу данных перед тестом
    print("База данных очищается")
    session.query(User).delete()
    session.commit()

    # Добавляем пользователей
    user_data_1 = {"first_name": "qqq", "last_name": "qqqq", "email": "qqq.smith@example.com"}
    user_data_2 = {"first_name": "www", "last_name": "www", "email": "www.johnson@example.com"}
    test_client.post("/users/", json=user_data_1)
    test_client.post("/users/", json=user_data_2)

    # Проверяем количество пользователей
    response = test_client.get("/users/")
    print("Данные в базе после добавления:", response.json())

    assert response.status_code == 200
    assert len(response.json()) == 2



# def test_create_user(test_client):  #  pytest -k "test_create_user"
#
#     # Данные для нового пользователя
#     user_data = {"first_name": "Иван", "last_name": "Дмитриевич", "email": "вануа.ывма@example.com"}
#
#     # Отправка POST-запроса на создание пользователя
#     response = test_client.post("/users/", json=user_data)
#
#     # Проверяем, что запрос выполнен успешно
#     assert response.status_code == 200
#
#     # Проверяем, что возвращенные данные совпадают с переданными
#     response_data = response.json()
#     assert response_data["first_name"] == user_data["first_name"]
#     assert response_data["last_name"] == user_data["last_name"]
#     assert response_data["email"] == user_data["email"]
#     assert "user_id" in response_data


def test_update_user(test_client):   # pytest -k "test_update_user"

    # Создаем пользователя
    user_data = {"first_name": "ННН", "last_name": "ЫВАПРО", "email": "АПРОЛ.johnson@example.com"}
    create_response = test_client.post("/users/", json=user_data)
    user_id = create_response.json()["user_id"]

    # Данные для обновления пользователя
    updated_user_data = {"first_name": "ННН", "last_name": "ЫВАПРО", "email": "АПРОЛ.johnson@example.com"}

    # Отправка PUT-запроса для обновления пользователя
    response = test_client.put(f"/users/{user_id}", json=updated_user_data)

    # Проверяем, что запрос выполнен успешно
    assert response.status_code == 200

    # Проверяем, что возвращенные данные обновлены
    response_data = response.json()
    assert response_data["first_name"] == updated_user_data["first_name"]
    assert response_data["last_name"] == updated_user_data["last_name"]
    assert response_data["email"] == updated_user_data["email"]

    # Дополнительная проверка в базе данных
    with TestingSessionLocal() as db:
        user = db.query(User).filter(User.user_id == user_id).first()
        assert user.first_name == updated_user_data["first_name"]
        assert user.last_name == updated_user_data["last_name"]
        assert user.email == updated_user_data["email"]





def test_delete(test_client):  # pytest -k "test_delete"
    # Добавление тестового пользователя
    user_data = {
        "first_name": "Дон",
        "last_name": "Дон",
        "email": "Дон.smith@example.com"
    }
    response = test_client.post("/users/", json=user_data)
    assert response.status_code == 200  # Убедимся, что пользователь был успешно создан

    user_id = response.json().get("user_id")  # Извлекаем user_id из ответа
    assert user_id is not None  # Убедимся, что user_id существует

    # Задержка для предотвращения блокировки базы данных
    time.sleep(1)

    # Отправка DELETE-запроса для удаления пользователя
    delete_response = test_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200  # Убедимся, что пользователь был удален успешно

    # Проверяем, что пользователь был удален
    get_response = test_client.get("/users/")
    response_data = get_response.json()
    assert all(user["user_id"] != user_id for user in response_data)  # Убедимся, что пользователя нет в списке