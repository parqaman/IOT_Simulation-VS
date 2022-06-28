import paho.mqtt.client as mqtt
import socket
import threading
from threading import Lock
import time

published_message = []
GATEWAY_IP = '172.30.0.2'
GATEWAY_PORT = 8080
DEVICE_IP = '172.30.0.6'

# Mutex for synchronizing the use of the published message list
mutex = Lock()

def notify_server(port, my_sock):
    my_sock.sendto(str(port).encode('utf-8'), (GATEWAY_IP, GATEWAY_PORT))
    data, address = my_sock.recvfrom(1024)
    decoded = data.decode()
    if(decoded == 'ACK'):
        return 0
    else:
        return -1

def udp_handler():
    # Look for open port and bind it
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((DEVICE_IP, 0))
    stat = notify_server(client_socket.getsockname()[1], client_socket)

    # if successfully notified gateway about the server
    if stat == 0:
        try:
            while True:
            # Waiting for data request from gateway
                data, address = client_socket.recvfrom(1024)
                the_message = ""
                if(address[0] == '172.30.0.2' and address[1] == 8080 and data.decode() == 'Data Request' and len(published_message) > 0):
                    mutex.acquire()
                    # Preparing reply message by taking message from the published message list
                    the_message = published_message[0][0] + ':' + published_message[0][1]
                    del published_message[0]
                    # Encode the message and send it to the gateway
                    mutex.release()

                client_socket.sendto(the_message.encode(), (address[0], address[1]))
                                    

        finally:
            print('Closing socket')

            # Close the socket after succesfully sending the message
            client_socket.close()
            return 0
    else:
        return -1

def on_connect(client, userdata, flags, rc):
    global t1
    global message_counter
    t1 = time.time()
    message_counter = 0
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('T')
    client.subscribe('WQ')
    client.subscribe('AQ')

def on_message(client, userdata, message):
    the_topic = message.topic
    content = message.payload.decode("utf-8")
    topic_message_tuple = (the_topic, content)
    # appending received message for later udp requests
    published_message.append(topic_message_tuple)

    global message_counter
    global t1
    message_counter = message_counter + 1
    t2 = time.time()
    the_time = t2 - t1
    print("Time in",str(message_counter) + "th message:", the_time)

def initialize_broker():
    mqttBroker = "mqtt.eclipseprojects.io"
    mqttPort = 1883
    subscriber = mqtt.Client()
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message # on message received handler
    subscriber.connect(mqttBroker, mqttPort)
    print('Connecting MQTT to {} on port {}'.format(mqttBroker, mqttPort))
    return subscriber

if __name__ == '__main__':
    my_subs = initialize_broker()

    # run udp handler in a different thread
    t = threading.Thread(target=udp_handler) 
    t.start()

    my_subs.loop_forever()

# Messung: In n Sekunden wie viele Nachrichten kann geschickt und empfangen werden?

# Beim jeden Datenhinzufügen P5
# 1. Fragen jedden datenbank, bist du da, wenn beide ja sind, update machen
# 2. Datenbank nehmen empfangene Daten in cache, aber noch nicht in DB gespeichert. Dann schickt die eine DB die empfaangene Daten zu der anderen DB. Erst nach der 2. DB die Ddaten empfangen hat, kann die Daten in beien DB gespeichert.
