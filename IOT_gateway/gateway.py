#!/usr/bin/python3

from random import randint
import socket
import time

DEVICE_IP = '172.30.0.3'
DEVICE_PORT = 8080

# Create the socket and post request
gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
devices = [('Temperature', "°C"), ('Humidity', "%"), ('Luminuous Intensity', "lm")]
while True:
    chosen_device, chosen_unit = devices[randint(0, 2)]

    # Ask for data from the chosen sensor device
    timestamp1 = time.time()
    gateway_socket.sendto(chosen_device.encode(), (DEVICE_IP, DEVICE_PORT))

    # Waiting for data from device 
    data, address = gateway_socket.recvfrom(1024)
    timestamp2 = time.time()

    RTT = timestamp2 - timestamp1
    print('RTT: ' + str(round(RTT*1000, 3)) + ' ms')
    print(chosen_device + ': ' + data.decode() + chosen_unit + '\n')
    
    time.sleep(2)