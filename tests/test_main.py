# import sys
# import os
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from fastapi.testclient import TestClient
# import time
#
# # Добавляем путь к user_app в sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../user_app")))
#
# from database import Base  # Импорт из папки user_app
# from main import app, get_db
# from user_app.models import User
#
# # Создаем тестовую базу данных
# SQLALCHEMY_DATABASE_URL_test = "sqlite:///./test_test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL_test, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# # Переопределяем зависимость get_db для тестов , для тестов будет использоваться не основная а наша новая бд
# def override_get_db():
#     print("Используется база данных:", SQLALCHEMY_DATABASE_URL_test)
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
#
#
# # Переопределяем зависимость в приложении  - сообщаем FastAPI, что вместо стандартной зависимости get_db нужно использовать override_get_db
# app.dependency_overrides[get_db] = override_get_db
#
#
# # test_client — это объект, созданный с помощью TestClient из библиотеки FastAPI. Он используется для имитации HTTP-запросов к вашему API во время тестирования.
# @pytest.fixture(scope="function")  # Это декоратор, который указывает, что test_client является фиктурой scope="function"
# def test_client(): # Эта фикстура гарантирует, что каждый тест работает в изолированной среде с чистой базой данных,
#     print(' База данных очищается')
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     print('База данных очищена')
#     client = TestClient(app)   # Создаёт объект TestClient, который позволяет отправлять запросы к вашему FastAPI-приложению (app) в тестовой среде.
#     yield client
#     # Удаление таблиц после теста
#     Base.metadata.drop_all(bind=engine)
#
#
#
#
#
#
# #  фикстура для базы данных  def test_get_users(test_client, session): этот тест не проходил без этого
#
# # Это декоратор, указывающий, что session является фиктурой.scope="module" означает, что фикстура создаётся один раз для всего тестового модуля
# @pytest.fixture(scope="module")
# def session():  # Эта фикстура помогает тестам работать с базой данных через одну сессию в рамках всего модуля, обеспечивая удобство, изоляцию и управляемость подключения к базе.
#     engine = create_engine("sqlite:///./test_test.db")
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     session = SessionLocal()
#     yield session
#     session.close()
#
#
#
# # Это декоратор, указывающий, что session является фикстурой scope="module"
# # означает, что фикстура создаётся один раз для всего тестового модуля (группы тестов в одном файле).
# # После завершения всех тестов в этом модуле фикстура очищается.
# # это нужно - чтобы использовать одну и ту же сессию базы данных в нескольких тестах внутри модуля, не пересоздавая её для каждого теста.
# # Это может ускорить выполнение тестов.
# @pytest.fixture(scope="module")
# def test_client():
#
#     with TestClient(app) as client:
#         yield client
#
#
#
#
#
#
# def test_create_user(test_client):           # pytest -k "test_create_user"   - проверка этой функции
#     # Данные для нового пользователя
#     user_data = {
#         "first_name": "Alice",
#         "last_name": "Smith",
#         "email": "alice.smith@example.com"
#     }
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
#
#
#
# # Тест для проверки получения пользователей
# def test_get_users(test_client, session):  # test_client: фикстура, возвращающая тестовый клиент (TestClient), который используется для отправки запросов к API.
#                                            # session: фикстура, возвращающая объект SQLAlchemy-сессии для взаимодействия с базой данных.
#     # Очищаем базу данных перед тестом
#     print("База данных очищается")
#     session.query(User).delete()  # Удаляет все записи из таблицы User в базе данных.
#     session.commit()              # Фиксирует изменения в базе данных
#
#     # Добавляем пользователей
#     user_data_1 = {"first_name": "qqq", "last_name": "qqqq", "email": "qqq.smith@example.com"}
#     user_data_2 = {"first_name": "www", "last_name": "www", "email": "www.johnson@example.com"}
#     test_client.post("/users/", json=user_data_1)  #  Отправляет POST-запрос
#     test_client.post("/users/", json=user_data_2)
#
#     # Проверяем количество пользователей
#     response = test_client.get("/users/")  # Отправляет GET-запрос к маршруту /users/, чтобы получить список всех пользователей из базы данных через API.
#     print("Данные в базе после добавления:", response.json())
#
#     assert response.status_code == 200
#     assert len(response.json()) == 2  # Проверяет, что длина списка пользователей в ответе равна 2.
#                                       # Это подтверждает, что два пользователя были успешно добавлены в базу данных.
#
#
#
# # def test_create_user(test_client):  #  pytest -k "test_create_user"
# #
# #     # Данные для нового пользователя
# #     user_data = {"first_name": "Иван", "last_name": "Дмитриевич", "email": "вануа.ывма@example.com"}
# #
# #     # Отправка POST-запроса на создание пользователя
# #     response = test_client.post("/users/", json=user_data)
# #
# #     # Проверяем, что запрос выполнен успешно
# #     assert response.status_code == 200
# #
# #     # Проверяем, что возвращенные данные совпадают с переданными
# #     response_data = response.json()
# #     assert response_data["first_name"] == user_data["first_name"]
# #     assert response_data["last_name"] == user_data["last_name"]
# #     assert response_data["email"] == user_data["email"]
# #     assert "user_id" in response_data
#
#
# def test_update_user(test_client):   # pytest -k "test_update_user"
#
#     # Создаем пользователя
#     user_data = {"first_name": "ННН", "last_name": "ЫВАПРО", "email": "АПРОЛ.johnson@example.com"}
#     create_response = test_client.post("/users/", json=user_data)
#     user_id = create_response.json()["user_id"]  # Получает ID созданного пользователя из ответа API (create_response).
#                                                  # ID пользователя нужен для отправки запроса на обновление данных (в маршруте /users/{user_id}).
#
#     # Данные для обновления пользователя
#     updated_user_data = {"first_name": "Первый", "last_name": "Второй", "email": "Третий.johnson@example.com"}
#
#     # Отправка PUT-запроса для обновления пользователя
#     response = test_client.put(f"/users/{user_id}", json=updated_user_data)
#
#     # Проверяем, что запрос выполнен успешно
#     assert response.status_code == 200
#
#     # Проверяем, что возвращенные данные обновлены
#     response_data = response.json()
#
#     # Сравнивает данные из ответа API с ожидаемыми данными (updated_user_data).
#     assert response_data["first_name"] == updated_user_data["first_name"]
#     assert response_data["last_name"] == updated_user_data["last_name"]
#     assert response_data["email"] == updated_user_data["email"]
#
#     # Дополнительная проверка в базе данных
#     with TestingSessionLocal() as db:
#         user = db.query(User).filter(User.user_id == user_id).first()
#         assert user.first_name == updated_user_data["first_name"]
#         assert user.last_name == updated_user_data["last_name"]
#         assert user.email == updated_user_data["email"]
#
#
#
#
#
# def test_delete(test_client):  # pytest -k "test_delete"
#     # Добавление тестового пользователя
#     user_data = {
#         "first_name": "Дон",
#         "last_name": "Дон",
#         "email": "Дон.smith@example.com"
#     }
#     response = test_client.post("/users/", json=user_data)
#     assert response.status_code == 200  # Убедимся, что пользователь был успешно создан
#
#     user_id = response.json().get("user_id")  # Извлекаем user_id из ответа
#     assert user_id is not None  # Убедимся, что user_id существует
#
#     # Задержка для предотвращения блокировки базы данных
#     time.sleep(1)
#
#     # Отправка DELETE-запроса для удаления пользователя
#     delete_response = test_client.delete(f"/users/{user_id}")
#     assert delete_response.status_code == 200  # Убедимся, что пользователь был удален успешно
#
#     # Проверяем, что пользователь был удален
#     get_response = test_client.get("/users/")
#     response_data = get_response.json()
#     assert all(user["user_id"] != user_id for user in response_data)  # Убедимся, что пользователя нет в списке