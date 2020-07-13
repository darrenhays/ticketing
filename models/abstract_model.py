import boto3
import logging
import uuid

logger = logging.getLogger()


class InvalidAttributeError(Exception):
    pass


class RequiredAttributeError(Exception):
    pass


class AbstractModel:
    table_name = None
    required_attributes = []
    optional_attributes = []

    def __init__(self):
        database = boto3.resource('dynamodb')
        self.table = database.Table(self.table_name)

    def insert(self, item):
        logger.info("########## {} insert ##########".format(self.__class__.__name__))
        logger.info("item: {}".format(item))
        if not self.contains_required_attributes(item):
            raise RequiredAttributeError('the following attributes are required: ' + ', '.join(self.required_attributes))
        if not self.attributes_are_valid(item):
            raise InvalidAttributeError('only the following attributes are allowed: ' + ', '.join(self.required_attributes + self.optional_attributes))
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
        if not self.attributes_are_valid(updated_attributes):
            raise InvalidAttributeError('only the following attributes are allowed: ' + ', '.join(self.required_attributes + self.optional_attributes))
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

    def contains_required_attributes(self, attributes):
        for attribute in self.required_attributes:
            if attribute not in attributes.keys():
                return False
        return True

    def attributes_are_valid(self, attributes):
        if not self.required_attributes and not self.optional_attributes:
            return True
        for key in attributes.keys():
            if key not in self.required_attributes + self.optional_attributes:
                return False
        return True
