#!/usr/bin/env python3
""" Test's module """
import requests


BASE_URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """ Test register_user method """
    url = "{}/users".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test log_in_wrong_password method """
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test log in method """
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.json().status_code == 200
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """ Test profile unlogged """
    url = "{}/sessions".format(BASE_URL)
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test profile logged """
    url = "{}/profile".format(BASE_URL)
    response = requests.get(url, cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["email"] == "guillaume@holberton.io"


def log_out(session_id: str) -> None:
    """ Test log out """
    url = "{}/sessions".format(BASE_URL)
    response = requests.delete(url, cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Bienvenue"


def reset_password_token(email: str) -> str:
    """ Test reset password token """
    url = "{}/reset_password".format(BASE_URL)
    data = {"email": email}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json()["email"] == email
    assert "reset_token" in response.json()
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test update password """
    url = "{}/reset_password".format(BASE_URL)
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
