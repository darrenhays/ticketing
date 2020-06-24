class AbstractModel:
    
    def __init__(self, database='dynamodb'):
        self.database = boto3.resource(database) # Not sure if this is correct of if I should create this within the methods themselves

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
