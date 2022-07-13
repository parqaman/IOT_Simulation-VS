#!/usr/bin/python3

from random import randint
import socket
import time

#DEVICE_PORT_LIST = []
DEVICE_ADDR_LIST = []
#DEVICE_IP = '172.30.0.3'

IP = '172.30.0.2'
PORT = 8080
SERVER_IP = '172.30.0.4'
SERVER_PORT = 50000
    
if __name__ == '__main__':
    # Create and bind the socket
    gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gateway_socket.bind((IP, PORT))
    print("Gateway started")

    # Wait for all sensor devices to report their ports
    num_of_sensors = 4
    while len(DEVICE_ADDR_LIST) < num_of_sensors:
        # Waiting for port data from device 
        data, address = gateway_socket.recvfrom(1024)
        DEVICE_ADDR_LIST.append(address)
        #DEVICE_PORT_LIST.append(data.decode())
        gateway_socket.sendto('ACK'.encode(), (address[0], address[1]))

    print("All devices have notified their address")
        
    # Requesting data
    while True:
        # UDP
        chosen_addr = DEVICE_ADDR_LIST[randint(0, len(DEVICE_ADDR_LIST) - 1)]
        print('chosen addr:', chosen_addr)

        # Ask for data from the chosen sensor device
        timestamp1 = time.time()
        gateway_socket.sendto("Data Request".encode(), (chosen_addr[0], int(chosen_addr[1])))

        # Waiting for data from sensor device 
        incoming_data, address = gateway_socket.recvfrom(1024)
        timestamp2 = time.time()

        RTT = timestamp2 - timestamp1
        print('UDP RTT: ' + str(round(RTT*1000, 3)) + ' ms')

        # TCP (HTTP)
        # HTTP request header
        request_line = 'POST /index.html?data={} HTTP/1.1'.format(incoming_data.decode())

        # Creating TCP socket
        gateway_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gateway_socket_tcp.connect((SERVER_IP, SERVER_PORT))

        # Sending payload to cloud server
        tcp_timestamp1 = time.time()
        gateway_socket_tcp.sendall(request_line.encode())

        # Waiting for response from cloud server
        server_response = gateway_socket_tcp.recv(1024).decode()
        tcp_timestamp2 = time.time()

        tcp_RTT = tcp_timestamp2 - tcp_timestamp1
        print('TCP POST RTT: ' + str(round(tcp_RTT*1000, 3)))
        #print(server_response + '\n')

        gateway_socket_tcp.close()

        # Requesting data from chosen address (device) every 2 seconds
        time.sleep(2)