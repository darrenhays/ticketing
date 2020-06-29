import logging
from boto3.dynamodb.conditions import Key
from models.abstract_model import AbstractModel

logger = logging.getLogger()


class UserModel(AbstractModel):
    def __init__(self):
        self.table_name = 'Users'
        super().__init__()
    
    def create_user(self, email, password):
        item = {
            'email': email,
            'password': password
        }
        return self.insert(item)
    
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
        return self.update(user_id, updated_attributes)
