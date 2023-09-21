import json
import os

import requests
from jsonschema.validators import validate

from tests.conftest import resources_path


def test_users_list():
    per_page = 6

    response = requests.get(
        url="https://reqres.in/api/users",
        params={"per_page": per_page}
    )

    assert response.status_code == 200
    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page

    
def test_users_list_schema():
    with open(os.path.join(resources_path, 'get_list_users.json')) as file:
        schema = json.loads(file.read())

    response = requests.get('https://reqres.in/api/users')
    validate(response.json(), schema)


def test_create_user():
    response = requests.post(
        'https://reqres.in/api/users',
        {"name": "Doja",
         "job": "Cat"}
    )

    assert response.status_code == 201
    assert response.json()['name'] == 'Doja'
    assert response.json()['job'] == 'Cat'


def test_create_user_schema():
    with open(os.path.join(resources_path, 'post_new_user.json')) as file:
        schema = json.loads(file.read())

        response = requests.post(
            'https://reqres.in/api/users',
            {"name": "Doja",
             "job": "Cat"}
        )
        validate(response.json(), schema)


def test_update_user():
    response = requests.patch(
        'https://reqres.in/api/users/2',
        {"name": "Amala Doja",
         "job": "Cat"}
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Amala Doja'
    assert response.json()['job'] == 'Cat'


def test_update_user_schema():
    with open(os.path.join(resources_path, 'patch_user_data.json')) as file:
        schema = json.loads(file.read())

        response = requests.patch(
            'https://reqres.in/api/users/2',
            {"name": "Amala Doja",
             "job": "Cat"}
        )
        validate(response.json(), schema)


def test_delete_user():
    response = requests.delete(
        'https://reqres.in/api/users/2'
    )

    assert response.status_code == 204


def test_successful_registration():
    response = requests.post(
        'https://reqres.in/api/register',
        {
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )

    assert response.status_code == 200
    assert response.json()['token'] is not None


def test_unsuccessful_registration():
    response = requests.post(
        'https://reqres.in/api/register',
        {
            "email": "eve.holt@reqres.in",
            "password": ""
        }
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_successful_login():
    response = requests.post(
        'https://reqres.in/api/login',
        {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    )

    assert response.status_code == 200
    assert response.json()['token'] == "QpwL5tke4Pnpja7X4"


def test_unsuccessful():
    response = requests.post(
        'https://reqres.in/api/login',
        {
            "email": "peter@klaven",
            "password": ""
        }
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'







