import boto3
import json
from settings import QUEUE_URL


class Queue:
    def __init__(self):
        self.client = boto3.client('sqs')
        
    def send_message(self, message):
        return self.client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

    def receive_message(self):
        return self.client.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1
        )

    def delete_message(self, message_id):
        return self.client.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message_id
        )
