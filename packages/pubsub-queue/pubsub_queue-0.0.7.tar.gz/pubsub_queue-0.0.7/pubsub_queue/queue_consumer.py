from google.cloud import pubsub_v1
from google.api_core.exceptions import DeadlineExceeded

class QueueConsumer:

    def __init__(self, project_id, subscription_name, topic_name):
        self.project_id = project_id
        self.subscription_name = subscription_name
        self.topic_name = topic_name
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(
            self.project_id, self.subscription_name
        )
        self.create_subscription_if_not_exists()
        
    def create_subscription_if_not_exists(self):
        project_path = self.subscriber.project_path(self.project_id)

        topic_path = self.subscriber.topic_path(self.project_id, self.topic_name)
        
        for subscription in self.subscriber.list_subscriptions(project_path):
            if subscription.name == self.subscription_path:
                return

        subscription = self.subscriber.create_subscription(
            self.subscription_path, topic_path
        )

    def work(self, callback_worker, num_messages=1, acknowledge_before=True):
        try:
            response = self.subscriber.pull(self.subscription_path, max_messages=num_messages)
        except DeadlineExceeded:
            print('End of messages')
            return

        while True:
            try:
                for message in response.received_messages:
                    if acknowledge_before:
                        self.subscriber.acknowledge(
                            self.subscription_path, [message.ack_id]
                        )

                    value = message.message.data.decode('utf-8')
                    print('Starting to work on "{}"'.format(value))
                    try:
                        callback_worker(value)
                        if acknowledge_before == False:
                            self.subscriber.acknowledge(
                                self.subscription_path, [message.ack_id]
                            )

                    except Exception as e:
                        print('Error on "{}" - {}'.format(value, e))
                                       
                response = self.subscriber.pull(self.subscription_path, max_messages=num_messages)
            except DeadlineExceeded:
                print('End of messages')
                break
