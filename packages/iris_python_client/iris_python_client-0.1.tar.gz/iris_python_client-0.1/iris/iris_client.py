import iris_settings
import logging
import boto3
import time
import json
import uuid
from collections import OrderedDict


class IrisClient:

    def __init__(self, settings=iris_settings):

        self.iris_queue = None
        self.iris_topic = None
        self.settings = settings

        if not self.settings.IRIS_BYPASS:
            self.sns_client = boto3.client('sns', self.settings.AWS_REGION)
            self.sqs = boto3.resource('sqs', self.settings.AWS_REGION)

    def get_queue(self):
        if self.iris_queue is None:
            self.iris_queue = self.sqs.get_queue_by_name(QueueName=self.settings.IRIS_SQS_APP_QUEUE)
        return self.iris_queue

    def get_topic(self):
        if self.iris_topic is None:
            self.iris_topic = self.sns_client.create_topic(Name=self.settings.IRIS_SNS_TOPIC).get('TopicArn')
        return self.iris_topic

    @staticmethod
    def get_new_session_id():

        return str(uuid.uuid4())

    def send_iris_message(self, message):

        if self.settings.IRIS_BYPASS:
            logging.info("Send message bypassed")
            return
        message['timestamp'] = int(round(time.time() * 1000))
        response = self.sns_client.publish(
            TopicArn=self.get_topic(),
            Message=json.dumps(message)
        )

        return response.get('MessageId')

    def read_iris_messages(self, count=5):

        if self.settings.IRIS_BYPASS:
            return None

        messages = self.get_queue().receive_messages(WaitTimeSeconds=self.settings.IRIS_POLL_INTERVAL,
                                                     MaxNumberOfMessages=count)
        unwrapped_messages = []
        for message in messages:
            # unwrap SNS and SQS bodies, get payload
            # add in message id to body
            # return
            unwrapped_message = {'message': json.loads(json.loads(message.body, object_pairs_hook=OrderedDict)
                                                       .get('Message')),
                                 'sqs_message': message}
            unwrapped_message['message']['message_id'] = message.message_id
            unwrapped_messages.append(unwrapped_message)

        return unwrapped_messages


class IrisListener:

    def __init__(self, settings=iris_settings):

        self.set_logging()
        self.iris = IrisClient(settings=settings)
        self.stop = False
        self.settings = settings

    def run(self, callback, message_filter=None):

        try:
            while not self.stop:

                if self.settings.IRIS_BYPASS:
                    time.sleep(self.settings.IRIS_POLL_INTERVAL)
                    continue

                for message in self.iris.read_iris_messages():
                    if message is not None:
                        # noinspection PyBroadException
                        # broad except as no knowledge of callback
                        try:
                            if message_filter is None or len(message_filter) == 0 \
                                    or message['message']['message_type'] \
                                    in message_filter:
                                callback(message['message'])
                        except:
                            logging.exception("Error processing Iris message")
                        finally:
                            message['sqs_message'].delete()

        except Exception as e:
            logging.exception("Error getting Iris messages")
            raise e

    @staticmethod
    def set_logging():

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', )
        logging.getLogger('boto').setLevel(logging.ERROR)
        logging.getLogger('botocore').setLevel(logging.ERROR)
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
