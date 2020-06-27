from models.abstract_model import AbstractModel
from objects.user import User


class UserModel(AbstractModel):
    def __init__(self):
        self.table_name = 'Users'
        super().__init__()
    
    def create_user(self, email, password):
        item = {
            'email': email,
            'password': password
        }
        user_id = self.insert(item)
        return User(user_id, email, password)
    
    def get_user(self, user_id):
        user_record = self.get(user_id)
        return User(user_record.get('id'), user_record.get('email'), user_record.get('password'))
    
    def delete_user(self, user_id):
        return self.delete(user_id)

    def update_user(self, user_id, updated_attributes):
        user_record = self.update(user_id, updated_attributes)
        return User(user_record.get('id'), user_record.get('email'), user_record.get('password'))
