from models.process_model import ProcessModel
from objects.queue import Queue


class BulkRefundProcessor:
    def process_bulk_refund(self, user_id, event_id):
        process_attributes = {
            "process_type": "refund_event",
            "event_id": event_id,
            "parent_process_id": "None",
            "status": "processing"
        }
        process_record = ProcessModel().create_process(process_attributes)
        refund_event_message = {
            "message_type": "refund_event",
            "user_id": user_id,
            "body": {
                "process_id": process_record.get('id'),
                "event_id": event_id
            }
        }
        Queue().send_message(refund_event_message)
        return process_record
