import psycopg2

DB_NAME = "tickets_db"
DB_USER = "postgres"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"


# Obtener conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


# Crear tabla de tickets
def create_table():
    conexion = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ticket (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                priority VARCHAR(255) NOT NULL,
                status VARCHAR(255) NOT NULL,
                server_worker VARCHAR(255) NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
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
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO ticket
            (
                title,
                description,
                priority,
                status,
                server_worker
            )
            VALUES (%s, %s, %s, %s, %s)
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
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ticket")
        return cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if conexion:
            conexion.close()