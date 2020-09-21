import boto3
import json
from settings import LAMBDA_URL, QUEUE_URL

client = boto3.client('sqs')


class BulkRefundProcessor:
    def process_bulk_refund(self, event_id):
        message_body = {
            "message_type": "event",
            "id": event_id,
            "base_url": LAMBDA_URL,
            "queue_url": QUEUE_URL
        }
        response = client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message_body)
        )

        return response
