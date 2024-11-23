from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import random
import threading

# Configuración de la app de Flask y SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Variables globales
smoke_level = 0
alert_message = ""

# Callback para conexión exitosa
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con el código: {rc}")
    client.subscribe("casa/sensorHumo")

# Callback para mensaje recibido
def on_message(client, userdata, msg):
    global smoke_level, alert_message
    # Decodificar el mensaje recibido
    message = msg.payload.decode()
    print(f"Mensaje recibido en el tema {msg.topic}: {message}")
    
    # Extraemos el nivel de humo y verificamos si hay alerta
    if "Nivel de humo" in message:
        smoke_level = int(message.split(":")[1].strip().split()[0])
        alert_message = "ALERTA!" if smoke_level > 800 else ""
        # Emitimos los datos al frontend
        socketio.emit('update_data', {'smoke_level': smoke_level, 'alert_message': alert_message})

# Callback para la publicación exitosa de un mensaje
def on_publish(client, userdata, mid):
    print(f"Mensaje publicado, id: {mid}")

# Inicializamos el cliente MQTT
client = mqtt.Client()

# Configuración de usuario y contraseña para autenticación en HiveMQ
client.username_pw_set("camilo", "Kamilopulistar17")

# Establecemos los callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Habilitamos TLS para conexión segura
client.tls_set()

# Conectamos al broker de HiveMQ
def connect_mqtt():
    try:
        client.connect("8ddb2eff8f8a4e05b2e3a1113f1b33f7.s1.eu.hivemq.cloud", 8883)
        client.loop_start()
    except Exception as e:
        print(f"Error al conectar al broker: {e}")
        exit(1)

# Hilo para la conexión MQTT
mqtt_thread = threading.Thread(target=connect_mqtt)
mqtt_thread.start()

# Ruta principal para servir la página web
@app.route('/')
def index():
    return render_template('index.html')

# Ejecutar la app de Flask con SocketIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
