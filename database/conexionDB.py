import sqlite3

DB = "database/tickets.db"

# □ Pool de hilos
# □ RabbitMQ
# □ PostgreSQL
# □ Nginx
# □ Diagrama final
# □ (Opcional) S3

def create_table():
    conexion = None
    try:
        conexion = sqlite3.connect(DB)
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description VARCHAR(255) NOT NULL,
                priority VARCHAR(255) NOT NULL,
                status VARCHAR(255) NOT NULL,
                server_worker VARCHAR(255) NOT NULL,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """)
        conexion.commit()
        print("Base de datos lista")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conexion:
            conexion.close()


# Guardar un ticket
def save_ticket(contenido):
    """
    contenido:
    (
        title,
        description,
        priority,
        status,
        server_worker
    )
    """
    conexion = None
    try:
        conexion = sqlite3.connect(DB)
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO ticket (title, description, priority, status, server_worker)
            VALUES (?, ?, ?, ?, ?)
            """,
            contenido,
        )
        conexion.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conexion:
            conexion.close()


# Obtener todos los tickets
def get_tickets():
    conexion = None
    try:
        conexion = sqlite3.connect(DB)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ticket")
        return cursor.fetchall()
    
    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if conexion:
            conexion.close()
