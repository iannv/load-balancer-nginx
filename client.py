import socket
import time
import json

HOST = "localhost"
PORT = 5000


def validate_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                client_socket.connect((HOST, PORT))
                print("Conectado al servidor")
                return client_socket

            except ConnectionRefusedError:
                print("Servidor no disponible. Reintentando en 3 segundos...")
                time.sleep(3)

    except Exception as e:
        print(f"Error al validar el servidor: {e}")
        return None


def configure_ticket(client_socket):
    try:
        generate_new_ticket = True
        while generate_new_ticket:
            print("\n****** SISTEMA DE TICKETS DE SOPORTE ******")
            print("\n============== NUEVO TICKET ==============")

            title = input("Título: ")

            if title.lower() == "salir":
                break

            description = input("Descripción: ")

            ticket = {
                "title": title,
                "description": description,
            }

            client_socket.send(json.dumps(ticket).encode())

            response = client_socket.recv(1024)

            print("\nRespuesta servidor:")
            print(response.decode())

            generate_ticket = input("¿Quiere generar un nuevo ticket? [S/N] : ")
            if generate_ticket.lower() == "s":
                generate_new_ticket = True
            else:
                generate_new_ticket = False

    except Exception as e:
        print(f"Error al enviar ticket: {e}")

    finally:
        client_socket.close()


def main():
    client = validate_server()

    if client:
        configure_ticket(client)


if __name__ == "__main__":
    main()
