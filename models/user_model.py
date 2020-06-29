from models.abstract_model import AbstractModel


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
    
    def delete_user(self, user_id):
        return self.delete(user_id)

    def update_user(self, user_id, updated_attributes):
        return self.update(user_id, updated_attributes)
