import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_root(client):
    response = client.get("/")
    print(response.json())
    assert response.status_code == 200

def test_create_user(client):
    email = "example15@email.com"
    password = "password"
    response = client.post("/users/", json={"email": email, "password": password})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == email
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("login/", data={"username": test_user["email"], "password": test_user["password"]})
    print(response.json())
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ("wrong@pytest.net", "password", 401),
    ("fixture@pytest.com", "wrong", 401),
    ("wrong@pytest.net", "wrong", 401),
    (None, "password", 401),
    ("fixture@pytest.com", None, 401)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("login/", data={"username": email, "password": password})
    print(res.json())
    print(res.status_code)
    assert res.status_code == status_code
    assert res.json().get("detail") == "Invalid Credentials"