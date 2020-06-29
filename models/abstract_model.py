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
            return {}         
        return item

    def get(self, id):
        logger.info("########## {} get ##########".format(self.__class__.__name__))
        logger.info("id: {}".format(id))
        try:
            return self.table.get_item(Key={'id': id})['Item']
        except Exception as e:
            logger.error(e)
            return {}

    def update(self, id, updated_attributes):
        logger.info("########## {} update ##########".format(self.__class__.__name__))
        logger.info("id: {}".format(id))
        item = self.get(id)
        for attribute, value in updated_attributes.items():
            item[attribute] = value
        try:
            self.table.put_item(Item=item)
        except Exception as e:
            logger.error(e)
            return {}
        return item

    def delete(self, id):
        logger.info("########## {} delete ##########".format(self.__class__.__name__))
        logger.info("id: {}".format(id))
        try:
            self.table.delete_item(Key={'id': id})
        except Exception as e:
            logger.error(e)
            return False
        return True
