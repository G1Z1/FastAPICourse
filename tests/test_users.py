from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from alembic import command
from app.database import get_db
from app.main import app
from app import schemas
from app.config import settings
from app.database import Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@localhost:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def override_get_db():
     db = TestingSessionLocal()
     try:
          yield db
     finally:
          db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
     #runs before test
     Base.metadata.drop_all(bind=engine)
     Base.metadata.create_all(bind=engine)
    #  command.upgrade("head")
    #  command.upgrade("base")
     yield TestClient(app)
     #runs after test

# uri: str = "http://192.168.129.27:8000/"
uri: str = "http://127.0.0.1:8000/"

def test_root(client):
    response = client.get(f"{uri}")
    print(response.json())
    assert response.status_code==200

def test_create_user(client):
    email = "example15@email.com"
    password = "password"
    response = client.post(f"{uri}users/", json={"email": email, "password": password})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == email
    assert response.status_code==201