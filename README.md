# load-balancer-nginx


## Instalaciones requeridas
- RabbitMQ
- Nginix
- Python
- PostgressSQL

Instalar el driver de PostgresSQL
`py -m pip install psycopg2-binary`


# Configuración del Balanceador de Carga

El sistema utiliza Nginx como balanceador TCP.

Configuración:

* Puerto de entrada: 5000
* Worker 1: localhost:5001
* Worker 2: localhost:5002

Nginx distribuye las conexiones entrantes entre ambos servidores utilizando el bloque `stream`.

Archivo de configuración incluido:
`config/nginx.conf`


## Ejecución
#### RabbitMQ
Si RabbitMQ no arranca automáticamente, debemos levanarlo manualmente ingresando a la carpeta `sbin` de RabbitMQ que se encuentra en:
`C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.1\sbin`
En esta ruta abrimos la cmd e ingresamos `rabbitmq-server.bat`
Si arrancó correctamente, aparecerá algo parecido a `Starting broker... completed with 0 plugins.`

Para ejecutar Nginix (en caso de que no funcione desde la terminal del editor de código) abirmos la cmd en la carpeta donde se encuentar el ejecutable nginix.exe y ejecutamos:
`nginix.exe`
Para verificar que se esté ejecutando correctamente, en otro cmd
`netstat -ano | findstr 5000`
Deberias ver algo parecido a `TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING`

En el editor de código abrimos varis terminales distinta para cada archivo .py y ejecutamos
- `py -m messaging.rabbitmq_consumer`
- `py server1.py`
- `py server2.py`
- `py client.py`


Nginx distribuye las conexiones TCP entrantes entre los workers. Cada worker procesa los tickets utilizando un pool de hilos y publica los mensajes en RabbitMQ. El consumidor desacopla el procesamiento y persiste los tickets en la base de datos.

