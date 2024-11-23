import time
import paho.mqtt.client as mqtt
import random  # Usamos random para simular los niveles de humo

# Callback para conexión exitosa
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con el código: {rc}")
    # Nos suscribimos a un tema donde el servidor pueda recibir mensajes (si es necesario)
    client.subscribe("casa/sensorHumo")

# Callback para mensaje recibido
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en el tema {msg.topic}: {msg.payload.decode()}")

# Callback para la publicación exitosa de un mensaje
def on_publish(client, userdata, mid):
    print(f"Mensaje publicado, id: {mid}")

# Inicializamos el cliente MQTT
client = mqtt.Client()

# Configuración de usuario y contraseña para autenticación en HiveMQ
client.username_pw_set("camilo", "Kamilopulistar17")  # Reemplaza YOUR_PASSWORD con la contraseña de HiveMQ

# Establecemos los callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Habilitamos TLS para conexión segura
client.tls_set()

# Conectamos al broker de HiveMQ
client.connect("8ddb2eff8f8a4e05b2e3a1113f1b33f7.s1.eu.hivemq.cloud", 8883)

# Función para publicar los datos de los sensores de humo
def publish_smoke_data():
    # Simulamos un sensor de humo generando niveles aleatorios
    smoke_level = random.randint(0, 1000)  # Simulamos un valor entre 0 y 1000
    alert = "ALERTA!" if smoke_level > 800 else ""
    message = f"Nivel de humo: {smoke_level} {alert}"

    # Publicamos los datos en el tema 'casa/sensorHumo'
    client.publish("casa/sensorHumo", payload=message, qos=1)
    print(f"Publicado: {message}")

# Bucle principal de la aplicación
try:
    while True:
        publish_smoke_data()  # Publica los datos del sensor
        time.sleep(2)  # Espera 2 segundos antes de publicar otro dato
        client.loop()  # Mantiene la conexión activa
except KeyboardInterrupt:
    print("Interrumpido por el usuario")
    client.disconnect()
