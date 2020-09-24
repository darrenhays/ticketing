import json
from models.process_model import ProcessModel
from models.ticket_model import TicketModel
from objects.queue import Queue


def event_handler(event, context):
    body = json.loads(event['Records'][0]['body'])
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

        # # Delete received message from queue
        # receipt_handle = event['Records'][0]['receiptHandle']
        # Queue().delete_message(receipt_handle)
    elif message_type == 'ticket':
        ProcessModel().create_process({"test": "TICKET", "event_id": "123"})
    else:
        # process checker
        ProcessModel().create_process({"test": "CHECKER", "event_id": "123"})
        pass

    return {
        'statusCode': 200,
        'body': event
    }
