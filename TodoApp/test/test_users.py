from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithpepi'
    assert response.json()['email'] == 'codingwithpepi@gmail.com'
    assert response.json()['first_name'] == 'Preslav'
    assert response.json()['last_name'] == 'Ivanchev'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '08954796314'

def test_change_password_success(test_user):
    response = client.put("/users/password", json={"password":"test1234","new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/password", json={"password":"wrong_password","new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}

def test_change_phone_number_success(test_user):
    response = client.put("/users/phone_number", json={"new_phone_number": "132121321312"})
    assert response.status_code == status.HTTP_204_NO_CONTENT