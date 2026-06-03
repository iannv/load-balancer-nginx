import json
import pika


def send_ticket(ticket):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="tickets", durable=True)
    channel.basic_publish(exchange="", routing_key="tickets", body=json.dumps(ticket))

    print("Ticket enviado a RabbitMQ")

    connection.close()
