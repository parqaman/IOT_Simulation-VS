#!/usr/bin/python3

from random import randint
import socket
import time

DEVICE_IP = '172.30.0.3'
DEVICE_PORT = 8080

# Create the socket and post request
gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
devices = ['Temperature', 'Humidity', 'Luminuous Intensity']
while True:
    chosen_device = devices[randint(0, 2)]

    # Ask for data from the chosen sensor device
    gateway_socket.sendto(chosen_device.encode(), (DEVICE_IP, DEVICE_PORT))
    timestamp1 = time.time()

    # Waiting for data from device 
    data, address = gateway_socket.recvfrom(1024)
    timestamp2 = time.time()

    RTT = timestamp2 - timestamp1
    print('RTT: ' + str(round(RTT*1000, 3)) + ' ms')
    print(chosen_device + ': ' + data.decode() + '\n')
    
    time.sleep(2)