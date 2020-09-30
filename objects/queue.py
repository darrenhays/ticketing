import boto3
import json
from settings import QUEUE_URL

client = boto3.client('sqs')


class Queue:
    def send_message(self, message):
        return client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

    def receive_message(self):
        return client.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1
        )

    def delete_message(self, receipt_handle):
        return client.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
