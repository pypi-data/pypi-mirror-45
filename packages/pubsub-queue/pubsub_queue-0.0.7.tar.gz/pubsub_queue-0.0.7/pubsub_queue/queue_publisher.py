from google.cloud import pubsub_v1

class QueuePublisher:

    def __init__(self, project_id, topic_name):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        self.topic_name = topic_name
        self.topic_path = self.publisher.topic_path(
            self.project_id,
            self.topic_name
        )
        self.create_topic_if_not_exists()

        def callback(message_future):
            if message_future.exception(timeout=30):
                print('Publishing message on {} threw an Exception {}.'.format(
                    topic_name, message_future.exception()))
            else:
                print(message_future.result())

        self.set_callback(callback)

    def set_callback(self, callback):
        self.callback = callback

    def create_topic_if_not_exists(self):
        project_path = self.publisher.project_path(self.project_id)
        for topic in self.publisher.list_topics(project_path):
            if self.topic_path == topic.name:
                return
        self.publisher.create_topic(self.topic_path)

    def publish(self, message_list):
        for message in message_list:
            message_future = self.publisher.publish(
                self.topic_path, data=message.encode('utf-8')
            )
            message_future.add_done_callback(self.callback)