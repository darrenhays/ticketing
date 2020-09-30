import json
import logging
from models.process_model import ProcessModel
from models.ticket_model import TicketModel
from models.user_model import UserModel
from objects.emailer import Emailer
from objects.queue import Queue
from objects.refund_processor import RefundProcessor, ItemsNotAvailable, ProcessingFailure
from settings import SYSTEM_EMAIL

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger = logging.getLogger()


def refund_event(message):
    logger.info("########## refund_event ##########")
    logger.info("message: {}".format(message))
    event_id = message['body']['event_id']
    process_attributes = {
        "process_type": message['message_type'],
        "event_id": event_id,
        "parent_process_id": "None",
        "status": "processing"
    }
    process_record = ProcessModel().create_process(process_attributes)
    parent_process_id = process_record.get('id')

    # send ticket messages to queue
    tickets = TicketModel().get_tickets_by_event(event_id)
    for ticket in tickets:
        ticket_message = {
            "message_type": "refund_ticket",
            "body": {
                "parent_process_id": parent_process_id,
                "ticket_id": ticket.get('id')
            }
        }
        Queue().send_message(ticket_message)

    # send process check message to queue
    process_checker_message = {
        "message_type": "process_checker",
        "user_id": message['user_id'],
        "body": {
            "parent_process_id": parent_process_id
        }
    }
    Queue().send_message(process_checker_message)


def refund_ticket(message):
    logger.info("########## refund_ticket ##########")
    logger.info("message: {}".format(message))
    ticket_id = message['body']['ticket_id']
    ticket_record = TicketModel().get_ticket(ticket_id)
    parent_process_id = message['body']['parent_process_id']
    process_attributes = {
        "process_type": message['message_type'],
        "ticket_id": ticket_id,
        "parent_process_id": parent_process_id,
        "status": "processing"
    }
    process_record = ProcessModel().create_process(process_attributes)

    # refund ticket
    purchase_id = ticket_record.get('purchase_id')
    try:
        RefundProcessor().process_refund(purchase_id, [ticket_id])  # process refund takes a list of ticket ids
    except (ItemsNotAvailable, ProcessingFailure) as e:
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


def send_process_report(message, failed_processes):
    logger.info("########## send_process_report ##########")
    logger.info("message: {}".format(message))
    logger.info("failed_processes: {}".format(failed_processes))
    user_id = message.get('user_id')
    email_address = UserModel().get_user(user_id).get('email')
    parent_process_id = message.get('body').get('parent_process_id')
    if failed_processes:
        subject = 'Cancel Event: Failure'
        message_body = 'Parent Process ID: {}'.format(parent_process_id)
        message_body += '<br /><b>Failed Processes</b><br />'
        message_body += '<br />'.join(failed_processes)
        Emailer().send_email(SYSTEM_EMAIL, 'ADMIN - ' + subject, message_body)
    else:
        subject = 'Cancel Event: Success'
        message_body = 'Parent Process ID: {} has been successfully cancelled.'.format(parent_process_id)
    Emailer().send_email(email_address, subject, message_body)


def process_checker(message):
    logger.info("########## process_checker ##########")
    logger.info("message: {}".format(message))
    parent_process_id = message['body']['parent_process_id']
    processes = ProcessModel().get_processes_by_parent_process(parent_process_id)
    failed_processes = []
    for process in processes:
        status = process.get('status')
        if status == 'processing':
            message = {
                "message_type": "process_checker",
                "user_id": message['user_id'],
                "body": {
                    "parent_process_id": parent_process_id
                }
            }
            Queue().send_message(message)
            return
        if status == 'failed':
            failed_processes.append(process.get('id'))
    else:
        process_attributes = {
            "process_type": message['message_type'],
            "parent_process_id": parent_process_id,
            "status": "completed"
        }
        ProcessModel().create_process(process_attributes)
        if failed_processes:
            updated_parent_process_status = {"status": "failed"}
        else:
            updated_parent_process_status = {"status": "completed"}
        ProcessModel().update_process(parent_process_id, updated_parent_process_status)
        send_process_report(message, failed_processes)


def event_handler(event, context):
    logger.info("########## bulk_process_event_handler ##########")
    logger.info("event: {}".format(event))
    message = json.loads(event['Records'][0]['body'])
    message_type = message['message_type']
    
    if message_type == 'refund_event':
        refund_event(message)
    elif message_type == 'refund_ticket':
        refund_ticket(message)
    elif message_type == 'process_checker':
        process_checker(message)
    return {
        'statusCode': 200,
        'body': event
    }
