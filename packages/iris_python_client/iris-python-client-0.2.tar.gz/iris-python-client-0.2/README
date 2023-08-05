# Iris

Iris - simple json message bus

This project is a thin wrapper around Amazon AWS SNS/SQS to provide a simple message bus.

Each Iris instance has an SNS topic, and a series of queues, one per listener, which are subscribed to that topic. Messages sent to the topic are re-sent to listeners via their queues. All listeners receive all messages, there is not routing.  

* _example_iris_settings.py_ is an example of the settings required for Iris. The default _iris_settings.py_ file obtains these from environment variables.
* _demo_send_iris_message.py_ demonstrates a how to send an Iris message
* _demo_iris_listener.py_ demonstrates how to create a simple Iris listener.