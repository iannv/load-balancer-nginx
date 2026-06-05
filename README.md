# Sistema Distribuido de Gestión de Tickets de Soporte

## Descripción

Este proyecto implementa un sistema distribuido de gestión de tickets utilizando múltiples componentes de infraestructura y comunicación.

La solución permite que clientes envíen tickets mediante conexiones TCP. Las solicitudes son distribuidas por un balanceador de carga Nginx hacia múltiples servidores trabajadores (workers), los cuales procesan las conexiones de forma concurrente utilizando un pool de hilos.

Los tickets son enviados a RabbitMQ para desacoplar la recepción del procesamiento y posteriormente son almacenados en PostgreSQL mediante un consumidor dedicado.

---

## Diagrama
<img width="1482" height="789" alt="image" src="https://github.com/user-attachments/assets/766b4bc4-525f-4659-8d6b-c386fd6f212c" />

---

## Tecnologías Utilizadas

* Python 3
* Socket TCP
* ThreadPoolExecutor
* RabbitMQ
* PostgreSQL
* Nginx
* JSON

---

## Componentes

### Cliente

Permite crear tickets desde consola enviando la información al balanceador de carga mediante TCP.

Datos enviados:

* Título
* Descripción

### Nginx

Actúa como balanceador de carga distribuyendo las conexiones TCP entrantes entre los servidores disponibles.

Configuración:

* Puerto de entrada: 5000
* Worker 1: localhost:5001
* Worker 2: localhost:5002

### Servidor 1 y Servidor 2

Reciben conexiones TCP provenientes de Nginx.

Funciones:

* Recepción de conexiones
* Validación de tickets
* Manejo concurrente mediante pool de hilos
* Publicación de mensajes en RabbitMQ

### RabbitMQ

Implementa una cola de mensajes para desacoplar la recepción de tickets del almacenamiento en la base de datos.

Cola utilizada:

* tickets

### Consumer

Consume los mensajes de RabbitMQ y persiste la información en PostgreSQL.

### PostgreSQL

Base de datos encargada de almacenar los tickets recibidos.

Tabla principal:

* ticket

Campos:

* id
* title
* description
* priority
* status
* server_worker
* date_created

---

## Instalaciones Requeridas

Instalar previamente:

* Python 3
* PostgreSQL
* RabbitMQ
* Nginx

Instalar dependencias de Python:

```bash
py -m pip install psycopg2-binary
py -m pip install pika
```

---

## Configuración de PostgreSQL

Crear una base de datos llamada:

```text
tickets_db
```

Crear la tabla:

```sql
CREATE TABLE IF NOT EXISTS ticket (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    server_worker VARCHAR(50) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Configuración del Balanceador de Carga

El sistema utiliza Nginx como balanceador TCP.

Archivo de configuración:

```text
config/nginx.conf
```

Configuración utilizada:

```nginx
stream {
    upstream workers {
        server 127.0.0.1:5001;
        server 127.0.0.1:5002;
    }

    server {
        listen 5000;
        proxy_pass workers;
    }
}
```

---

## Ejecución

### 1. Iniciar RabbitMQ

Abrir una consola en:

```text
C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.1\sbin
```

Ejecutar:

```bash
rabbitmq-server.bat
```

Si inició correctamente aparecerá un mensaje similar a:

```text
Starting broker... completed
```

---

### 2. Iniciar Nginx

Abrir una consola en la carpeta donde se encuentra:

```text
nginx.exe
```

Ejecutar:

```bash
nginx.exe
```

Verificar que esté escuchando:

```bash
netstat -ano | findstr 5000
```

Resultado esperado:

```text
TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING
```

---

### 3. Iniciar Consumer

```bash
py -m messaging.rabbitmq_consumer
```

---

### 4. Iniciar Workers

Servidor 1:

```bash
py server1.py
```

Servidor 2:

```bash
py server2.py
```

---

### 5. Ejecutar Cliente

```bash
py client.py
```

---

## Flujo de Funcionamiento

1. El cliente crea un ticket y lo envía mediante TCP.
2. Nginx recibe la conexión y la distribuye entre los servidores disponibles.
3. El servidor procesa la solicitud utilizando un hilo del pool.
4. El ticket es publicado en RabbitMQ.
5. El consumidor recupera el mensaje desde la cola.
6. El ticket es almacenado en PostgreSQL.
7. El cliente recibe una confirmación de recepción.

---
