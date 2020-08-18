import logging
from models.abstract_model import AbstractModel
from settings import PURCHASES_TABLE_NAME

logger = logging.getLogger()


class PurchaseModel(AbstractModel):
    table_name = PURCHASES_TABLE_NAME
    required_attributes = [
        'timestamp',
        'purchased_items',
        'total'
    ]
    optional_attributes = [
        'user_id',
        'refunded_items'
    ]

    def create_purchase(self, attributes):
        logger.info("########## {} create_purchase ##########".format(self.__class__.__name__))
        logger.info("attributes: {}".format(attributes))
        return self.insert(attributes)

    def get_purchase(self, purchase_id):
        logger.info("########## {} get_purchase ##########".format(self.__class__.__name__))
        logger.info("purchase_id: {}".format(purchase_id))
        return self.get(purchase_id)

    def delete_purchase(self, purchase_id):
        logger.info("########## {} delete_purchase ##########".format(self.__class__.__name__))
        logger.info("purchase_id: {}".format(purchase_id))
        return self.delete(purchase_id)

    def update_purchase(self, purchase_id, updated_attributes):
        logger.info("########## {} update_purchase ##########".format(self.__class__.__name__))
        logger.info("purchase_id: {}".format(purchase_id))
        logger.info("updated_attributes: {}".format(updated_attributes))
        return self.update(purchase_id, updated_attributes)
