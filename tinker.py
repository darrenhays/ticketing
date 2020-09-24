from objects.queue import Queue
from models.process_model import ProcessModel
from models.ticket_model import TicketModel
import time
import json

message = {"message_type": "ticket",
           "id": "c01506e3-c95b-4be6-9396-2f8e0e685827"}

Queue().send_message(message)
time.sleep(3)
event = Queue().receive_message()
body = json.loads(event['Messages'][0]['Body'])
message_type = body['message_type']

if message_type == 'ticket':
    ticket_id = body['id']
    ticket_record = TicketModel().get_ticket(ticket_id)
    event_id = ticket_record.get('event_id')
    process_attributes = {
        "process_type": message_type,
        "ticket_id": ticket_id,
        "event_id": event_id,
        "status": "processing"
    }
    process_record = ProcessModel().create_process(process_attributes)

    # refund ticket


