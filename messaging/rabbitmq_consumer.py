from database import conexionDB
import json
import pika


# Procesar cada ticket recibido desde RabbitMQ
def process_ticket(ch, method, properties, body):
    try:
        ticket = json.loads(body.decode())

        print("\n===== TICKET RECIBIDO DESDE RABBITMQ =====")
        print(f"Título: {ticket['title']}")
        print(f"Descripción: {ticket['description']}")
        print(f"Servidor: {ticket['server_worker']}")

        conexionDB.save_ticket(
            (
                ticket["title"],
                ticket["description"],
                ticket["priority"],
                ticket["status"],
                ticket["server_worker"],
            )
        )
        print("Ticket almacenado en la base de datos")

        # Confirmar procesamiento del mensaje
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error procesando ticket: {e}")


# Iniciar consumidor y escuchar la cola de tickets
def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        # Crear cola si no existe
        channel.queue_declare(queue="tickets", durable=True)
        channel.basic_consume(queue="tickets", on_message_callback=process_ticket)

        print("Esperando tickets...")
        channel.start_consuming()

    except Exception as e:
        print(f"Error RabbitMQ: {e}")


if __name__ == "__main__":
    start_consumer()
