import json
from models.process_model import ProcessModel
from models.ticket_model import TicketModel
from objects.queue import Queue
from objects.refund_processor import RefundProcessor, ItemsNotAvailable, ProcessingFailure


def event_handler(event, context):
    body = json.loads(event['Records'][0]['body'])
    message_type = body['message_type']

    if message_type == 'event':
        event_id = body['id']
        process_attributes = {
            "process_type": message_type,
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
    elif message_type == 'ticket':
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
        purchase_id = ticket_record.get('purchase_id')
        try:
            RefundProcessor().process_refund(purchase_id, [ticket_id])  # process refund takes a list of ticket ids
        except ItemsNotAvailable as e:
            updated_process_attributes = {"status": "failed", "error": e}
            ProcessModel().update_process(process_record.get('id'), updated_process_attributes)
            return
        except ProcessingFailure as e:
            updated_process_attributes = {"status": "failed", "error": e}
            ProcessModel().update_process(process_record.get('id'), updated_process_attributes)
            return

        # delete ticket
        try:
            TicketModel().delete_ticket(ticket_id)
        except:
            updated_process_attributes = {"status": "failed", "error": "deleteError"}
            ProcessModel().update_process(process_record.get('id'), updated_process_attributes)
            return

        # update process
        ProcessModel().update_process(process_record.get('id'), {"status": "completed"})
    else:
        event_id = body['id']
        processes = ProcessModel().get_processes_by_event(event_id)
        for process in processes:
            if process.get('status') == 'processing':
                message = {
                    "message_type": "checker",
                    "id": event_id
                }
                Queue().send_message(message)
                break
        else:
            process_attributes = {
                "process_type": message_type,
                "event_id": event_id,
                "status": "completed"
            }
            ProcessModel().create_process(process_attributes)
            #FIXME send email

    return {
        'statusCode': 200,
        'body': event
    }
