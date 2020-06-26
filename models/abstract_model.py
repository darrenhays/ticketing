import boto3
import logging
import uuid

logger = logging.getLogger()


class AbstractModel:
    table_name = None
    def __init__(self):
        database = boto3.resource('dynamodb')
        self.table = database.Table(self.table_name)

    def insert(self, item):
        logger.info("########## {} insert ##########".format(self.__class__.__name__))
        logger.info("item: {}".format(item))
        item['id'] = str(uuid.uuid4())
        try:
            self.table.put_item(Item=item)
        except Exception as e:
            logger.error(e)
            return None           
        return item['id']

    def get(self, id):
        logger.info("########## {} get ##########".format(self.__class__.__name__))
        logger.info("id: {}".format(id))
        try:
            return self.table.get_item(Key={'id': id})['Item']
        except Exception as e:
            logger.error(e)
            return {}

    def update(self, id, attributes_to_update, attribute_values):
        logger.info("########## {} update ##########".format(self.__class__.__name__))
        logger.info("id: {}".format(id))
        try:
            self.table.update_item(Key={'id': id}, UpdateExpression=attributes_to_update, ExpressionAttributeValues=attribute_values)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete(self, id):
        logger.info("########## {} delete ##########".format(self.__class__.__name__))
        logger.info("id: {}".format(id))
        try:
            self.table.delete_item(Key={'id': id})
        except Exception as e:
            logger.error(e)
            return False
        return True
