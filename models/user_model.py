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
        user_record = self.get(id)
        return User(user_record.get('id'), user_record.get('email'), user_record.get('password'))
    
    def delete_user(self, user):
        return self.delete(user.id)

    def update_user(self, user):
        attributes_to_update = "set email = :e, password = :p"
        attribute_values = {
            ':e': user.email,
            ':p': user.password
        }
        if self.update(user.id, attributes_to_update, attribute_values):
            return user
        return User()
