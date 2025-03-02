from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from alembic import command
from app.database import get_db
from app.main import app
from app.config import settings
from app.database import Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@localhost:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_dev"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
@pytest.fixture(scope="function") #scope="module"/"session" => db doesn't get destroyed after every individual test - "function" = default
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(session):
    # runs before test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # command.upgrade("head")
    # command.upgrade("base")
    yield TestClient(app) # Destroys and recreates db after every test
    #runs after test


@pytest.fixture # Preventing test_login from being dependent from test_create_user
def test_user(client):
    user_data = {"email": "fixture@pytest.com", "password": "password"}
    response = client.post("/users/", json=user_data)
    # print(response.json())
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture # Preventing test_login from being dependent from test_create_user
def test_user_extra(client):
    user_data = {"email": "fixture1@pytest.com", "password": "password"}
    response = client.post("/users/", json=user_data)
    # print(response.json())
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    # print(client.headers)
    # print(token)
    return client


@pytest.fixture
def test_posts(test_user, test_user_extra, session):
    posts_data = [
    {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    },
    {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    },
    {
        "title": "fourth title",
        "content": "fourth content",
        "owner_id": test_user_extra["id"]
    }]

    # def create_post_model(posts):
    #     models.Post(**posts)
    # posts = list(map(create_post_model, posts_data))
    
    posts = list(map(lambda p: models.Post(**p), posts_data))
    
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()