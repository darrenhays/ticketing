from objects.queue import Queue


class BulkRefundProcessor:
    def process_bulk_refund(self, event_id):
        message = {
            "message_type": "event",
            "id": event_id
        }
        return Queue().send_message(message)
