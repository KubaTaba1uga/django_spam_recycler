import pika

connection = pika.BlockingConnection(
    pika.connection.URLParameters('amqp://myuser:mypassword@localhost:5672/myvhost'))

channel = connection.channel()

arguments = {"x-single-active-consumer": False}

channel.queue_declare(
    queue='exclusive_consumer',
     arguments=arguments,
     durable=True,
        exclusive=True)


channel.basic_publish(
    exchange='',
     routing_key='hello',
     body='Hello World!')
print(" [x] Sent 'Hello World!'")

channel.start_consuming()
