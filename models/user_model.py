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
        id = self.insert(item)
        return User(id, email, password)
    
    def get_user(self, id):
        user = self.get(id)
        return User(user['id'], user['email'], user['password'])
        