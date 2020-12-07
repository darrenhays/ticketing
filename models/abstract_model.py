import boto3
import datetime
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
    __optional_attributes = [
        'status'
    ]
    __protected_attributes = [
        'created',
        'updated'
    ]

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
        item['created'] = item['updated'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        if not item.get('status'):
            item['status'] = 'active'
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
        item['updated'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
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
            self.update(id, {'status': "inactive"})
        except Exception as e:
            logger.error(e)
            return False
        return True

    def remove(self, id):
        logger.info("########## {} remove ##########".format(self.__class__.__name__))
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
            if key not in self.required_attributes + self.optional_attributes + self.__optional_attributes:
                return False
        return True
