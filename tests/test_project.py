import json
import requests
import unittest
from models.user_model import UserModel
from objects.user import User
from unittest.mock import patch


class TestProject(unittest.TestCase):
    @patch('models.user_model.AbstractModel.insert')
    @patch('models.user_model.UserModel.get_user_by_email')
    def test_user_model_creates_a_user_record(self, mock_get_user_by_email, mock_insert):
        user_id = 'some_id'
        user_email = 'test@test.com'
        user_password = 'testpassword'
        user_first_name = "First"
        user_last_name = "Last"
        
        mock_get_user_by_email.return_value = {}
        mock_insert.return_value = {
            'id': user_id,
            'email': user_email,
            'password': user_password,
            'first_name': user_first_name,
            'last_name': user_last_name
        }

        attributes = {
            'email': user_email,
            'password': user_password,
            'first_name': user_first_name,
            'last_name': user_last_name
        }

        user_record = UserModel().create_user(attributes)

        assert isinstance(user_record, dict)
        assert user_record['id']
        assert user_record['email'] == user_email
        assert user_record['password'] == user_password

    def test_create_authenticate_get_update_delete_user_delete_session_end_to_end(self):
        user_email = 'end_to_end_test_user@test.com'
        user_password = 'testpassword'
        user_first_name = 'first'
        user_last_name = 'last'

        # delete user if not successfully deleted in last run
        user = UserModel().get_user_by_email(user_email)
        if user:
            UserModel().delete_user(user.get('id'))

        # create user
        create_user_response = requests.request(
            url='http://localhost:5000/users',
            method='POST',
            data=json.dumps({
                "email": user_email,
                "password": user_password,
                "first_name": user_first_name,
                "last_name": user_last_name
            })
        )
        create_user_response_body = json.loads(create_user_response.text)
        user_id = create_user_response_body.pop('id')
        expected_create_user_response_body = {
            "email": user_email,
            "first_name": user_first_name,
            "last_name": user_last_name
        }

        # create session
        create_session_response = requests.request(
            url='http://localhost:5000/sessions',
            method='POST',
            data=json.dumps({
                "email": user_email,
                "password": user_password,
                "user_id": user_id
            })
        )
        create_session_response_body = json.loads(create_session_response.text)
        session_id = create_session_response_body.get('session_id')
        
        # get user
        get_user_response = requests.request(
            url='http://localhost:5000/users/{}'.format(user_id),
            method='GET',
            headers={
                "session_id": session_id
            }
        )
        get_user_response_body = json.loads(get_user_response.text)
        expected_get_user_response_body = {
            "id": user_id,
            "email": user_email,
            "first_name": user_first_name,
            "last_name": user_last_name
        }

        # update user
        user_email = "newtest@test.com"
        update_user_response = requests.request(
            url='http://localhost:5000/users/{}'.format(user_id),
            method='PATCH',
            data=json.dumps({
                "email": user_email,
                "password": user_password
            }),
            headers={
                "session_id": session_id
            }
        )
        update_user_response_body = json.loads(update_user_response.text)
        expected_update_user_response_body = {
            "id": user_id,
            "email": user_email,
            "first_name": user_first_name,
            "last_name": user_last_name
        }

        # delete user
        delete_user_response = requests.request(
            url='http://localhost:5000/users/{}'.format(user_id),
            method='DELETE',
            headers={
                "session_id": session_id
            }
        )
        delete_user_response_body = json.loads(delete_user_response.text)
        expected_delete_user_response_body = {'message': 'success'}

        # delete session
        delete_session_response = requests.request(
            url='http://localhost:5000/sessions/{}'.format(session_id),
            method='DELETE',
            headers={
                "session_id": session_id
            }
        )
        delete_session_response_body = json.loads(delete_session_response.text)
        expected_delete_session_response_body = {'message': 'success'}

        # testing create user
        assert create_user_response.status_code == 200
        assert create_user_response_body == expected_create_user_response_body
        assert json.loads(create_user_response.text)['id']

        # testing create session
        assert session_id

        # testing get user
        assert get_user_response.status_code == 200
        assert get_user_response_body == expected_get_user_response_body

        # testing update user
        assert update_user_response.status_code == 200
        assert update_user_response_body == expected_update_user_response_body

        # testing delete user
        assert delete_user_response.status_code == 200
        assert delete_user_response_body == expected_delete_user_response_body

        # testing delete session
        assert delete_user_response.status_code == 200
        assert delete_session_response_body == expected_delete_session_response_body
