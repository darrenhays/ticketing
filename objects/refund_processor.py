from models.purchase_model import PurchaseModel
from models.ticket_model import TicketModel
from objects.payment_handler import PaymentHandler


class ItemsNotAvailable(Exception):
    """raised when an item is not found in purchased items"""
    pass


class ProcessingFailure(Exception):
    """raised when a purchase is not created"""
    pass


class RefundProcessor:
    def process_refund(self, purchase_id, item_ids):
        purchase_record = PurchaseModel().get_purchase(purchase_id)
        updated_purchase_record = {}
        updated_purchase_record['purchased_items'] = purchase_record.get('purchased_items', [])
        updated_purchase_record['refunded_items'] = purchase_record.get('refunded_items', [])
        refund_total = 0.0
        refunded_ticket_ids = []
        for item_id in item_ids:
            for i, purchased_item in enumerate(updated_purchase_record['purchased_items']):
                if item_id == purchased_item.get('id'):
                    refund_total += float(purchased_item.get('amount_paid'))
                    updated_purchase_record['refunded_items'].append(updated_purchase_record['purchased_items'].pop(i))
                    refunded_ticket_ids.append(item_id)
                    break
            else:
                raise ItemsNotAvailable("one or more items are not available for refund")
        purchase_record = PurchaseModel().update_purchase(purchase_id, updated_purchase_record)
        if purchase_record:
            payment_id = purchase_record.get('payment_id')
            if PaymentHandler().process_refund(payment_id, refund_total):
                for ticket_to_delete in refunded_ticket_ids:
                    TicketModel().delete_ticket(ticket_to_delete)
                return purchase_record
        raise ProcessingFailure("could not process refund")
