import json
import requests
import unittest
import uuid
from models.user_model import UserModel
from settings import BASE_URL
from unittest.mock import patch


class TestProject(unittest.TestCase):
    base_url = BASE_URL
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
        user_email = 'end_to_end_test_user_{}@test.com'.format(str(uuid.uuid4()))
        updated_user_email = 'newtest_{}@test.com'.format(str(uuid.uuid4()))
        user_password = 'testpassword'
        user_first_name = 'first'
        user_last_name = 'last'

        # create user
        create_user_response = requests.request(
            url=self.base_url + '/users',
            method='POST',
            data=json.dumps({
                "email": user_email,
                "password": user_password,
                "first_name": user_first_name,
                "last_name": user_last_name
            })
        )
        create_user_response_body = json.loads(create_user_response.text)
        # popping these items as they are unknown
        user_id = create_user_response_body.pop('id')
        user_created = create_user_response_body.pop('created')
        user_updated = create_user_response_body.pop('updated')
        expected_create_user_response_body = {
            "email": user_email,
            "first_name": user_first_name,
            "last_name": user_last_name
        }

        # create session
        create_session_response = requests.request(
            url=self.base_url + '/sessions',
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
            url=self.base_url + '/users/{}'.format(user_id),
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
            "last_name": user_last_name,
            "created": user_created,
            "updated": user_updated
        }

        # update user
        user_email = updated_user_email
        update_user_response = requests.request(
            url=self.base_url + '/users/{}'.format(user_id),
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
        # popping these items as they are unknown
        update_user_response_body.pop('updated')
        expected_update_user_response_body = {
            "id": user_id,
            "email": user_email,
            "first_name": user_first_name,
            "last_name": user_last_name,
            "created": user_created
        }

        # create event
        event_title = "Test Event"
        event_capacity = "9000"
        event_description = "Live Donkey Show!"
        create_event_response = requests.request(
            url=self.base_url + '/events',
            method='POST',
            headers={
                "session_id": session_id
            },
            data=json.dumps({
                "title": event_title,
                "capacity": event_capacity,
                "description": event_description,
                "user_id": user_id
            })
        )
        create_event_response_body = json.loads(create_event_response.text)
        # popping these items as they are unknown
        event_id = create_event_response_body.pop('id')
        event_created = create_event_response_body.pop('created')
        event_updated = create_event_response_body.pop('updated')
        expected_create_event_response_body = {
                "title": event_title,
                "capacity": event_capacity,
                "description": event_description,
                "user_id": user_id
        }

        # get event
        get_event_response = requests.request(
            url=self.base_url + '/events/{}'.format(event_id),
            method='GET',
            headers={
                "session_id": session_id
            }
        )
        get_event_response_body = json.loads(get_event_response.text)
        expected_get_event_response_body = {
            "id": event_id,
            "title": event_title,
            "capacity": event_capacity,
            "description": event_description,
            "user_id": user_id,
            "created": event_created,
            "updated": event_updated
        }

        # update event
        event_title = "Updated Event Title"
        update_event_response = requests.request(
            url=self.base_url + '/events/{}'.format(event_id),
            method='PATCH',
            data=json.dumps({
                "title": event_title
            }),
            headers={
                "session_id": session_id
            }
        )
        update_event_response_body = json.loads(update_event_response.text)
        # popping these items as they are unknown
        update_event_response_body.pop('updated')
        expected_update_event_response_body = {
            "id": event_id,
            "title": event_title,
            "capacity": event_capacity,
            "description": event_description,
            "user_id": user_id,
            "created": event_created
        }

        # create ticket_type
        ticket_type_title = "Test Ticket Type"
        ticket_type_limit = "42"
        ticket_type_price = "100"
        ticket_type_description = "Front row seat"
        create_ticket_type_response = requests.request(
            url=self.base_url + '/events/{}/ticket-types'.format(event_id),
            method='POST',
            headers={
                "session_id": session_id
            },
            data=json.dumps({
                "title": ticket_type_title,
                "limit": ticket_type_limit,
                "description": ticket_type_description,
                "price": ticket_type_price,
                "event_id": event_id
            })
        )
        create_ticket_type_response_body = json.loads(create_ticket_type_response.text)
        # popping these items as they are unknown
        ticket_type_id = create_ticket_type_response_body.pop('id')
        ticket_type_created = create_ticket_type_response_body.pop('created')
        ticket_type_updated = create_ticket_type_response_body.pop('updated')
        expected_create_ticket_type_response_body = {
            "title": ticket_type_title,
            "limit": ticket_type_limit,
            "description": ticket_type_description,
            "price": ticket_type_price,
            "event_id": event_id
        }

        # get ticket type
        get_ticket_type_response = requests.request(
            url=self.base_url + '/events/{}/ticket-types/{}'.format(event_id, ticket_type_id),
            method='GET',
            headers={
                "session_id": session_id
            }
        )
        get_ticket_type_response_body = json.loads(get_ticket_type_response.text)
        expected_get_ticket_type_response_body = {
            "id": ticket_type_id,
            "title": ticket_type_title,
            "limit": ticket_type_limit,
            "description": ticket_type_description,
            "price": ticket_type_price,
            "event_id": event_id,
            "created": ticket_type_created,
            "updated": ticket_type_updated
        }

        # update ticket type
        ticket_type_title = "Updated Ticket Type Title"
        update_ticket_type_response = requests.request(
            url=self.base_url + '/events/{}/ticket-types/{}'.format(event_id, ticket_type_id),
            method='PATCH',
            data=json.dumps({
                "title": ticket_type_title
            }),
            headers={
                "session_id": session_id
            }
        )
        update_ticket_type_response_body = json.loads(update_ticket_type_response.text)
        # popping these items as they are unknown
        update_ticket_type_response_body.pop('updated')
        expected_update_ticket_type_response_body = {
            "id": ticket_type_id,
            "title": ticket_type_title,
            "limit": ticket_type_limit,
            "description": ticket_type_description,
            "price": ticket_type_price,
            "event_id": event_id,
            "created": ticket_type_created
        }

        # create purchase
        ticket_quantity = "2"
        create_purchase_response = requests.request(
            url=self.base_url + '/purchases',
            method='POST',
            headers={
                "session_id": session_id
            },
            data=json.dumps({
                "user_id": user_id,
                "items": [
                    {
                        "event_id": event_id,
                        "ticket_type_id": ticket_type_id,
                        "quantity": ticket_quantity
                    }
                ]
            })
        )
        create_purchase_response_body = json.loads(create_purchase_response.text)
        # popping these items as they are unknown
        purchase_id = create_purchase_response_body.pop('id')
        purchase_created = create_purchase_response_body.pop('created')
        purchase_updated = create_purchase_response_body.pop('updated')
        for item in create_purchase_response_body['purchased_items']:
            item.pop('id')
            item.pop('created')
            item.pop('updated')
        expected_create_purchase_response_body = {
            "user_id": user_id,
            "total": str(float(ticket_type_price) * int(ticket_quantity)),
            "purchased_items": [
                {
                    "event_id": event_id,
                    "ticket_type_id": ticket_type_id,
                    "event_title": event_title,
                    "event_description": event_description,
                    "ticket_type_title": ticket_type_title,
                    "ticket_type_description": ticket_type_description,
                    "amount_paid": ticket_type_price
                },
                {
                    "event_id": event_id,
                    "ticket_type_id": ticket_type_id,
                    "event_title": event_title,
                    "event_description": event_description,
                    "ticket_type_title": ticket_type_title,
                    "ticket_type_description": ticket_type_description,
                    "amount_paid": ticket_type_price
                }
            ],
            "refunded_items": []
        }

        # get purchase
        get_purchase_response = requests.request(
            url=self.base_url + '/purchases/{}'.format(purchase_id),
            method='GET',
            headers={
                "session_id": session_id
            }
        )
        get_purchase_response_body = json.loads(get_purchase_response.text)
        purchased_items = []  # to be used in refund purchase
        # popping these items as they are unknown
        get_purchase_response_body.pop('id')
        for item in get_purchase_response_body['purchased_items']:
            purchased_items.append(item.pop('id'))
            item.pop('created')
            item.pop('updated')
        expected_get_purchase_response_body = {
            "user_id": user_id,
            "total": str(float(ticket_type_price) * int(ticket_quantity)),
            "purchased_items": [
                {
                    "event_id": event_id,
                    "ticket_type_id": ticket_type_id,
                    "event_title": event_title,
                    "event_description": event_description,
                    "ticket_type_title": ticket_type_title,
                    "ticket_type_description": ticket_type_description,
                    "amount_paid": ticket_type_price
                },
                {
                    "event_id": event_id,
                    "ticket_type_id": ticket_type_id,
                    "event_title": event_title,
                    "event_description": event_description,
                    "ticket_type_title": ticket_type_title,
                    "ticket_type_description": ticket_type_description,
                    "amount_paid": ticket_type_price
                }
            ],
            "refunded_items": [],
            "created": purchase_created,
            "updated": purchase_updated
        }

        # refund purchase
        refund_purchase_response = requests.request(
            url=self.base_url + '/purchases/{}/refund'.format(purchase_id),
            method='POST',
            data=json.dumps(purchased_items),
            headers={
                "session_id": session_id
            }
        )
        refund_purchase_response_body = json.loads(refund_purchase_response.text)
        # popping these items as they are unknown
        refund_purchase_response_body.pop('updated')
        for item in refund_purchase_response_body['refunded_items']:
            item.pop('id')
            item.pop('created')
            item.pop('updated')

        expected_refund_purchase_response_body = {
            "user_id": user_id,
            "total": str(float(ticket_type_price) * int(ticket_quantity)),
            "purchased_items": [],
            "refunded_items": [
                {
                    "event_id": event_id,
                    "ticket_type_id": ticket_type_id,
                    "event_title": event_title,
                    "event_description": event_description,
                    "ticket_type_title": ticket_type_title,
                    "ticket_type_description": ticket_type_description,
                    "amount_paid": ticket_type_price
                },
                {
                    "event_id": event_id,
                    "ticket_type_id": ticket_type_id,
                    "event_title": event_title,
                    "event_description": event_description,
                    "ticket_type_title": ticket_type_title,
                    "ticket_type_description": ticket_type_description,
                    "amount_paid": ticket_type_price
                }
            ],
            "created": purchase_created,
            "id": purchase_id,
        }

        # delete ticket type
        delete_ticket_type_response = requests.request(
            url=self.base_url + '/events/{}/ticket-types/{}'.format(event_id, ticket_type_id),
            method='DELETE',
            headers={
                "session_id": session_id
            }
        )
        delete_ticket_type_response_body = json.loads(delete_ticket_type_response.text)
        expected_delete_ticket_type_response_body = {'message': 'success'}

        # delete event
        delete_event_response = requests.request(
            url=self.base_url + '/events/{}'.format(event_id),
            method='DELETE',
            headers={
                "session_id": session_id
            }
        )
        delete_event_response_body = json.loads(delete_event_response.text)
        expected_delete_event_response_body = {'message': 'success'}

        # delete user
        delete_user_response = requests.request(
            url=self.base_url + '/users/{}'.format(user_id),
            method='DELETE',
            headers={
                "session_id": session_id
            }
        )
        delete_user_response_body = json.loads(delete_user_response.text)
        expected_delete_user_response_body = {'message': 'success'}

        # delete session
        delete_session_response = requests.request(
            url=self.base_url + '/sessions/{}'.format(session_id),
            method='DELETE',
            headers={
                "session_id": session_id
            }
        )
        delete_session_response_body = json.loads(delete_session_response.text)
        expected_delete_session_response_body = {'message': 'success'}

        # clean up section
        UserModel().delete_user(user_id)

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

        # testing create event
        assert create_event_response.status_code == 200
        assert create_event_response_body == expected_create_event_response_body
        assert event_id

        # testing get event
        assert get_event_response.status_code == 200
        assert get_event_response_body == expected_get_event_response_body

        # testing update event
        assert update_event_response.status_code == 200
        assert update_event_response_body == expected_update_event_response_body

        # testing create ticket type
        assert create_ticket_type_response.status_code == 200
        assert create_ticket_type_response_body == expected_create_ticket_type_response_body
        assert ticket_type_id

        # testing get event
        assert get_ticket_type_response.status_code == 200
        assert get_ticket_type_response_body == expected_get_ticket_type_response_body

        # testing update ticket type
        assert update_ticket_type_response.status_code == 200
        assert update_ticket_type_response_body == expected_update_ticket_type_response_body

        # testing create purchase
        assert create_purchase_response.status_code == 200
        assert create_purchase_response_body == expected_create_purchase_response_body
        assert purchase_id

        # testing get purchase
        assert get_purchase_response.status_code == 200
        assert get_purchase_response_body == expected_get_purchase_response_body

        # testing refund purchase
        assert refund_purchase_response.status_code == 200
        assert refund_purchase_response_body == expected_refund_purchase_response_body

        # testing delete ticket type
        assert delete_ticket_type_response.status_code == 200
        assert delete_ticket_type_response_body == expected_delete_ticket_type_response_body

        # testing delete event
        assert delete_event_response.status_code == 200
        assert delete_event_response_body == expected_delete_event_response_body

        # testing delete user
        assert delete_user_response.status_code == 200
        assert delete_user_response_body == expected_delete_user_response_body

        # testing delete session
        assert delete_user_response.status_code == 200
        assert delete_session_response_body == expected_delete_session_response_body
