import json
import logging

logger = logging.getLogger()


class AbstractModelObject:
    __attributes = {}
    __allowed_attributes = [
        'id',
        'created',
        'updated',
        'status'
    ]
    sensitive_attributes = []
    allowed_attributes = [] + sensitive_attributes

    def __init__(self, attributes={}):
        logger.info("########## {} __init__ ##########".format(self.__class__.__name__))
        logger.info("attributes: {}".format(attributes))
        self.allowed_attributes.extend(['created', 'updated'])
        self.load(attributes)

    def __getattr__(self, key):
        logger.info("########## {} __getattr__ ##########".format(self.__class__.__name__))
        logger.info("key: {}".format(key))
        return self.__attributes[key]

    def __setattr__(self, key, value):
        logger.info("########## {} __setattr__ ##########".format(self.__class__.__name__))
        logger.info("key: {}".format(key))
        logger.info("value: {}".format(value))
        if key in self.allowed_attributes or key in self.__allowed_attributes:
            self.__attributes[key] = value

    @property
    def __dict__(self):
        logger.info("########## {} __dict__ ##########".format(self.__class__.__name__))
        return self.__attributes

    def load(self, attributes):
        logger.info("########## {} load ##########".format(self.__class__.__name__))
        logger.info("attributes: {}".format(attributes))
        for key, value in attributes.items():
            if key in self.allowed_attributes or key in self.__allowed_attributes:
                self.__attributes[key] = value

    @property
    def attributes(self):
        logger.info("########## {} attributes ##########".format(self.__class__.__name__))
        return self.__dict__

    def jsonify(self):
        logger.info("########## {} jsonify ##########".format(self.__class__.__name__))
        attributes = self.__dict__
        for attribute in self.sensitive_attributes:
            attributes.pop(attribute, None)
        return json.dumps(attributes)
