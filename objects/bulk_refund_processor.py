from objects.queue import Queue


class BulkRefundProcessor:
    def process_bulk_refund(self, user_id, event_id):
        message = {
            "message_type": "refund_event",
            "user_id": user_id,
            "body": {
                "event_id": event_id
            }
        }
        return Queue().send_message(message)
