import pika

connection = pika.BlockingConnection(
    pika.connection.URLParameters('amqp://myuser:mypassword@localhost:5672/myvhost'))

channel = connection.channel()

arguments = {"x-single-active-consumer": True}

channel.queue_declare(
    queue='single_consumer',
     arguments=arguments,
     durable=True)

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
