import boto3
import uuid


class AbstractModel:
    table_name = None
    def __init__(self):
        database = boto3.resource('dynamodb')
        self.table = database.Table(self.table_name)

    def insert(self, item):
        item['id'] = str(uuid.uuid4())
        self.table.put_item(Item=item)
        return item['id']

    def get(self, id):
        return self.table.get_item(Key={'id': id})['Item']

    def update(self):
        pass

    def delete(self):
        pass
