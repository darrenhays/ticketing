import logging
from boto3.dynamodb.conditions import Key
from models.abstract_model import AbstractModel
from objects.password import Password
from settings import USERS_TABLE_NAME

logger = logging.getLogger()


class EmailExistsError(Exception):
    pass


class UserModel(AbstractModel):
    table_name = USERS_TABLE_NAME
    required_attributes = [
        'email',
        'password'
    ]
    optional_attributes = [
        'first_name',
        'last_name',
        'parent_user_id'
    ]

    def create_user(self, attributes={}):
        if self.get_user_by_email(attributes.get('email')):
            raise EmailExistsError('email already exists')
        attributes['password'] = str(Password(attributes.get('password')))
        return self.insert(attributes)

    def get_user(self, user_id):
        return self.get(user_id)

    def get_user_by_email(self, email):
        logger.info("########## {} get_user_by_email ##########".format(self.__class__.__name__))
        logger.info("email: {}".format(email))
        key = Key('email').eq(email)
        try:
            response = self.table.query(IndexName='email-index', KeyConditionExpression=key)
            return response.get('Items')[0]
        except Exception as e:
            logger.error(e)
            return {}
    
    def delete_user(self, user_id):
        return self.delete(user_id)

    def update_user(self, user_id, updated_attributes):
        user_record_by_email = self.get_user_by_email(updated_attributes.get('email'))
        if user_record_by_email and user_record_by_email.get('id') != user_id:
            raise EmailExistsError('email already exists')
        if updated_attributes.get('password'):
            updated_attributes['password'] = str(Password(updated_attributes.get('password')))
        return self.update(user_id, updated_attributes)
