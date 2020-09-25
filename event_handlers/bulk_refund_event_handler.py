import json
import logging
from models.event_model import EventModel
from models.process_model import ProcessModel
from models.ticket_model import TicketModel
from models.user_model import UserModel
from objects.emailer import Emailer
from objects.queue import Queue
from objects.refund_processor import RefundProcessor, ItemsNotAvailable, ProcessingFailure
from settings import SYSTEM_EMAIL

logger = logging.getLogger()


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
            "message_type": "checker",
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
    elif message_type == 'checker':
        event_id = body['id']
        processes = ProcessModel().get_processes_by_event(event_id)
        failed_processes = []
        for process in processes:
            status = process.get('status')
            if status == 'processing':
                message = {
                    "message_type": "checker",
                    "id": event_id
                }
                Queue().send_message(message)
                break
            if status == 'failed':
                failed_processes.append(process.get('id'))
        else:
            process_attributes = {
                "process_type": message_type,
                "event_id": event_id,
                "status": "completed"
            }
            ProcessModel().create_process(process_attributes)
            user_id = EventModel().get_event(event_id).get('user_id')
            email_address = UserModel().get_user(user_id).get('email')
            if failed_processes:
                subject = 'Cancel Event: Failure'
                message_body = 'Event ID: {}'.format(event_id)
                message_body += '<br /><b>Failed Processes</b><br />'
                message_body += '<br />'.join(failed_processes)
                Emailer().send_email(SYSTEM_EMAIL, 'ADMIN - ' + subject, message_body)
            else:
                subject = 'Cancel Event: Success'
                message_body = 'Event ID: {} has been successfully cancelled.'.format(event_id)
            Emailer().send_email(email_address, subject, message_body)
    return {
        'statusCode': 200,
        'body': event
    }
