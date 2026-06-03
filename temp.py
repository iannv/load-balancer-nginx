from messaging.rabbitmq_producer import send_ticket

ticket = {
    "title": "Error login",
    "description": "No puedo ingresar"
}

send_ticket(ticket)