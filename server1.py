import socket
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from database import conexionDB
from messaging.rabbitmq_producer import send_ticket

HOST = "localhost"
PORT = 5001
SERVER_NAME = "server_1"
MAX_WORKERS = 5


# Configuración de IP y puerto TCP del servidor
def initialize_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        conexionDB.create_table()
        server_socket.listen(5)

        print(f"{SERVER_NAME} iniciado en {HOST}:{PORT}")
        print("Esperando conexiones...")

        return server_socket

    except OSError as e:
        print(f"Error {e} - El puerto {PORT} ya está en uso")

    except Exception as e:
        print(f"Error en la base de datos: {e}")


# Aceptar las conexiones del cliente
def accept_connection(server_socket):
    try:
        executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

        while True:
            conn_client, addr_client = server_socket.accept()
            print(f"\nCliente conectado desde " f"{addr_client[0]}:{addr_client[1]}")

            executor.submit(socket_client, conn_client, addr_client)

    except Exception as e:
        print(f"Error al aceptar conexión: {e}")


# Recibir ticket del cliente, validar contenido, almacenar en la base de datos y enviar confirmación
def socket_client(conn_client, addr_client):
    try:
        while True:
            data = conn_client.recv(1024)

            if not data:
                break

            ticket = json.loads(data.decode())
            title = ticket.get("title", "").strip()
            description = ticket.get("description", "").strip()

            if not title or not description:
                conn_client.send("**** Ticket inválido ****".encode())
                continue

            print("\n========= TICKET =========")
            print(f"Título: {title}")
            print(f"Descripción: {description}")
            print(f"IP Cliente: {addr_client[0]}")
            print(f"Servidor: {SERVER_NAME}")

            send_ticket(
                {
                    "title": title,
                    "description": description,
                    "priority": "MEDIUM",
                    "status": "PENDING",
                    "server_worker": SERVER_NAME,
                }
            )

            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            response = (
                f"Ticket recibido correctamente " f"por {SERVER_NAME} " f"- {timestamp}"
            )

            conn_client.send(response.encode())

    except json.JSONDecodeError:
        conn_client.send("Formato JSON inválido".encode())

    except Exception as e:
        print(f"Error en el socket cliente: {e}")

    finally:
        conn_client.close()


def main():
    server = initialize_server()

    if server:
        accept_connection(server)


if __name__ == "__main__":
    main()
