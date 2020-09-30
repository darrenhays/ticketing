import boto3
import logging
from botocore.exceptions import ClientError
from settings import SYSTEM_NAME, SYSTEM_EMAIL

logger = logging.getLogger()


class Emailer:
    def __init__(self):
        self.client = boto3.client('ses')
        self.sender = "{} <{}>".format(SYSTEM_NAME, SYSTEM_EMAIL)
        self.charset = "UTF-8"

    def send_email(self, recipient, subject, body_text):
        logger.info("########## {} send_email ##########".format(self.__class__.__name__))
        logger.info("recipient: {}".format(recipient))
        logger.info("subject: {}".format(subject))
        logger.info("body_text: {}".format(body_text))
        body_html = """
            <html>
                <head></head>
                <body>
                    <p>{}</p>
                </body>
            </html>""".format(body_text)
        message = {
            'Body': {
                'Html': {
                    'Charset': self.charset,
                    'Data': body_html,
                },
                'Text': {
                    'Charset': self.charset,
                    'Data': body_text,
                },
            },
            'Subject': {
                'Charset': self.charset,
                'Data': subject,
            }
        }
        try:
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message=message,
                Source=self.sender
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            logger.error("###### {}.send_email: failure".format(self.__class__.__name__))
            logger.error(e.response['Error']['Message'])
        else:
            logger.info("###### {}.send_email: success".format(self.__class__.__name__))
            return(response['MessageId'])
