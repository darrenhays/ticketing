import json
import requests
import unittest
from models.user_model import UserModel
from objects.user import User
from unittest.mock import patch


class TestProject(unittest.TestCase):
    @patch('models.user_model.AbstractModel.insert')
    def test_user_model_creates_a_user_object(self, mock_insert):
        mock_insert.return_value = 'some_id'

        user_email = 'test@test.com'
        user_password = 'testpassword'
        user = UserModel().create_user(user_email, user_password)

        assert isinstance(user, User)
        assert user.id
        assert user.email == user_email
        assert user.password == user_password

    def test_create_get_delete_user_end_to_end(self):
        user_email = 'test@test.com'
        user_password = 'testpassword'
        
        # create user
        create_user_response = requests.request(
            url='http://localhost:5000/users',
            method='POST',
            data=json.dumps({
                "email": user_email,
                "password": user_password
            })
        )
        create_user_response_body = json.loads(create_user_response.text)
        user_id = create_user_response_body.pop('id')
        expected_create_user_response_body = {
            "email": user_email,
            "password": user_password
        }
        
        # get user
        get_user_response = requests.request(
            url='http://localhost:5000/users/{}'.format(user_id),
            method='GET'
        )
        get_user_response_body = json.loads(get_user_response.text)
        expected_get_user_response_body = {
            "id": user_id,
            "email": user_email,
            "password": user_password
        }

        # update user
        user_email = "newtest@test.com"
        update_user_response = requests.request(
            url='http://localhost:5000/users/{}'.format(user_id),
            method='PATCH',
            data=json.dumps({
                "email": user_email,
                "password": user_password
            })
        )
        update_user_response_body = json.loads(update_user_response.text)
        expected_update_user_response_body = {
            "id": user_id,
            "email": user_email,
            "password": user_password
        }

        # delete user
        delete_user_response = requests.request(
            url='http://localhost:5000/users/{}'.format(user_id),
            method='DELETE'
        )
        delete_user_response_body = json.loads(delete_user_response.text)
        expected_delete_user_response_body = {'message': 'success'}

        # testing create user
        assert create_user_response.status_code == 200
        assert create_user_response_body == expected_create_user_response_body
        assert json.loads(create_user_response.text)['id']

        # testing get user
        assert get_user_response.status_code == 200
        assert get_user_response_body == expected_get_user_response_body

        # testing update user
        assert update_user_response.status_code == 200
        assert update_user_response_body == expected_update_user_response_body

        # testing delete user
        assert delete_user_response.status_code == 200
        assert delete_user_response_body == expected_delete_user_response_body