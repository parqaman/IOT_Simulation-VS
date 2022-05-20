#!/usr/bin/python3

from random import randint
import socket
import time

DEVICE_PORT_LIST = []

DEVICE_IP = '172.30.0.3'

IP = '172.30.0.2'
PORT = 8080

# Create and bind the socket
gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gateway_socket.bind((IP, PORT))

# Wait for all sensor devices to report their ports
num_of_sensors = 3
while len(DEVICE_PORT_LIST) < num_of_sensors:
    # Waiting for port data from device 
    data, address = gateway_socket.recvfrom(1024)
    DEVICE_PORT_LIST.append(data.decode())
    gateway_socket.sendto('ACK'.encode(), (address[0], address[1]))
    
# Requesting data
while True:
    chosen_port = DEVICE_PORT_LIST[randint(0, len(DEVICE_PORT_LIST) - 1)]

    # Ask for data from the chosen sensor device
    timestamp1 = time.time()
    gateway_socket.sendto("Data Request".encode(), (DEVICE_IP, int(chosen_port)))

    # Waiting for data from sensor device 
    data, address = gateway_socket.recvfrom(1024)
    timestamp2 = time.time()

    RTT = timestamp2 - timestamp1
    print('Data from port:', address[1])
    print('RTT: ' + str(round(RTT*1000, 3)) + ' ms')
    print(data.decode() + '\n')
    time.sleep(2)