from audioop import add
import paho.mqtt.client as mqtt
import socket
import threading
from threading import Lock

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


def on_message(client, userdata, message):
    the_topic = message.topic
    content = message.payload.decode("utf-8")
    print("Received message:", content, " from topic", the_topic)
    topic_message_tuple = (the_topic, content)
    mutex.acquire()
    # appending received message for later udp requests
    published_message.append(topic_message_tuple)
    mutex.release()

def initialize_broker():
    mqttBroker = "mqtt.eclipseprojects.io"
    mqttPort = 1883
    subscriber = mqtt.Client()
    subscriber.on_message = on_message # on message received handler
    subscriber.connect(mqttBroker, mqttPort)
    print('Connecting MQTT to {} on port {}'.format(mqttBroker, mqttPort))
    return subscriber

if __name__ == '__main__':
    my_subs = initialize_broker()

    # subscribe to all sensors
    my_subs.subscribe('T')
    my_subs.subscribe('WQ')
    my_subs.subscribe('AQ')

    # run udp handler ina different thread
    t1 = threading.Thread(target=udp_handler) 
    t1.start()

    my_subs.loop_forever()