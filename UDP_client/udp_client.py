#!/usr/bin/python3

import socket
from sensor import Sensor

# Set the IP and port
IP = '172.30.0.3'
PORT = 8080

# Create the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket with the ip and port
client_socket.bind((IP, PORT))

sensor_devices = {
  'Temperature': Sensor(1),
  'Humidity': Sensor(2),
  'Luminuous Intensity': Sensor(3)
  }

try:
  while True:
    # Waiting for data request from gateway
    data, address = client_socket.recvfrom(1024)
    decoded = data.decode()

    # Preparing reply message
    the_message = str(sensor_devices[decoded].get_sensor_value())

    # Encode the message and send it to the gateway
    client_socket.sendto(the_message.encode('utf-8'), (address[0], address[1]))
    
finally:
    print('Closing socket')

    # Close the socket after succesfully sending the message
    client_socket.close()