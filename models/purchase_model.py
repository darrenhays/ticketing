from models.abstract_model import AbstractModel
from settings import PURCHASES_TABLE_NAME


class PurchaseModel(AbstractModel):
    table_name = PURCHASES_TABLE_NAME
    required_attributes = [
        'purchased_items',
        'refunded_items',
        'total',
        'payment_id'
    ]
    optional_attributes = [
        'user_id',
        'status'
    ]

    def create_purchase(self, attributes):
        attributes['refunded_items'] = []
        return self.insert(attributes)

    def get_purchase(self, purchase_id):
        return self.get(purchase_id)

    def delete_purchase(self, purchase_id):
        return self.delete(purchase_id)

    def update_purchase(self, purchase_id, updated_attributes):
        return self.update(purchase_id, updated_attributes)
