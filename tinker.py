from objects.queue import Queue
from models.process_model import ProcessModel
from models.ticket_model import TicketModel
import time
import json

message = {"message_type": "event",
           "id": "c01506e3-c95b-4be6-9396-2f8e0e685827"}

Queue().send_message(message)
time.sleep(3)
event = Queue().receive_message()
body = json.loads(event['Messages'][0]['Body'])
message_type = body['message_type']

if message_type == 'event':
    event_id = body['id']
    process_attributes = {
        "process_type": "event",
        "event_id": event_id,
        "status": "processing"
    }
    process_record = ProcessModel().create_process(process_attributes)

    # send ticket messages to queue
    tickets = TicketModel().get_tickets_by_event(event_id)
    for ticket in tickets:
        message = {
            "message_type": "ticket",
            "id": ticket.get('id')
        }
        Queue().send_message(message)

    # send process check message to queue
    message = {
        "message_type": "process_check",
        "id": event_id
    }
    Queue().send_message(message)
    ProcessModel().update_process(process_record.get('id'), {"status": "completed"})

    # Delete received message from queue
    receipt_handle = event['Messages'][0]['ReceiptHandle']
    Queue().delete_message(receipt_handle)
