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


def event_handler(event, context):
    logger.info("########## bulk_process_event_handler ##########")
    logger.info("event: {}".format(event))

    message = json.loads(event['Records'][0]['body'])
    message_type = message['message_type']

    if message_type == 'refund_event':
        process_refund_event_message(message)
    elif message_type == 'refund_ticket':
        process_refund_ticket_message(message)
    elif message_type == 'complete_parent_process':
        process_complete_parent_process_message(message)
    return {
        'statusCode': 200,
        'body': event
    }


def process_refund_event_message(message):
    logger.info("########## process_refund_event_message ##########")
    logger.info("message: {}".format(message))

    event_id = message['body']['event_id']
    process_id = message['body']['process_id']

    tickets = TicketModel().get_tickets_by_event(event_id)
    for ticket in tickets:
        ticket_process_attributes = {
            "process_type": "refund_ticket",
            "ticket_id": ticket.get('id'),
            "parent_process_id": process_id,
            "status": "processing"
        }
        ticket_process_record = ProcessModel().create_process(ticket_process_attributes)
        ticket_message = {
            "message_type": "refund_ticket",
            "body": {
                "process_id": ticket_process_record.get('id'),
                "parent_process_id": process_id,
                "ticket_id": ticket.get('id')
            }
        }
        Queue().send_message(ticket_message)

    complete_parent_process_attributes = {
        "process_type": "complete_parent_process",
        "parent_process_id": process_id,
        "status": "processing"
    }
    complete_parent_process_record = ProcessModel().create_process(complete_parent_process_attributes)
    complete_parent_process_message = {
        "message_type": "complete_parent_process",
        "user_id": message['user_id'],
        "body": {
            "process_id": complete_parent_process_record.get('id'),
            "parent_process_id": process_id
        }
    }
    Queue().send_message(complete_parent_process_message)


def process_refund_ticket_message(message):
    logger.info("########## process_refund_ticket_message ##########")
    logger.info("message: {}".format(message))

    ticket_id = message['body']['ticket_id']
    ticket_record = TicketModel().get_ticket(ticket_id)
    process_id = message['body']['process_id']

    # refund ticket
    purchase_id = ticket_record.get('purchase_id')
    try:
        RefundProcessor().process_refund(purchase_id, [ticket_id])  # process refund takes a list of ticket ids
    except (ItemsNotAvailable, ProcessingFailure) as e:
        updated_process_attributes = {"status": "failed", "error": e}
        ProcessModel().update_process(process_id, updated_process_attributes)
        return

    # delete ticket
    try:
        TicketModel().delete_ticket(ticket_id)
        updated_process_attributes = {"status": "completed"}
    except:
        updated_process_attributes = {"status": "failed", "error": "deleteError"}

    # update process
    ProcessModel().update_process(process_id, updated_process_attributes)


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


def process_complete_parent_process_message(message):
    logger.info("########## process_complete_parent_process_message ##########")
    logger.info("message: {}".format(message))

    process_id = message['body']['process_id']
    parent_process_id = message['body']['parent_process_id']
    processes = ProcessModel().get_processes_by_parent_process(parent_process_id)
    failed_processes = []

    for process in processes:
        if process.get('id') == process_id:
            continue
        current_status = process.get('status')
        if current_status == 'processing':
            logger.info("########## process_complete_parent_process_message: processes not completed ##########")
            logger.info("########## pushing message back in to queue ##########")
            message = {
                "message_type": "complete_parent_process",
                "user_id": message['user_id'],
                "body": {
                    "process_id": process_id,
                    "parent_process_id": parent_process_id
                }
            }
            Queue().send_message(message)
            return
        if current_status == 'failed':
            failed_processes.append(process.get('id'))
    else:
        logger.info("########## process_complete_parent_process_message: processes completed ##########")
        logger.info("########## cleaning up ##########")
        if failed_processes:
            updated_process_status = {"status": "failed"}
        else:
            updated_process_status = {"status": "completed"}
        ProcessModel().update_process(parent_process_id, updated_process_status)
        ProcessModel().update_process(process_id, {"status": "completed"})
        send_process_report(message, failed_processes)
