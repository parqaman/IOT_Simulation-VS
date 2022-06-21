#!/usr/bin/python3

import socket
import threading
import sys

IP = '172.30.0.4'
PORT = 50000
DATABASE_IP = '172.30.0.5'
DATABASE_PORT = 9090
sensor_data = []

# your gen-py dir
sys.path.append('gen-py')

# MyDBService files
from MyDBService import *
from MyDBService.ttypes import *

# Thrift files
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def write_in_html(in_file, in_data):
    write_html = open(in_file, "w")
    for i in range(len(html_string)):
        if html_string[i] == '        <h1>Sensor Devices Values</h1>\n':
            sensor_data.append(in_data)
            data_as_html = '<p>' + in_data + '</p>\n'
            html_string.insert(i+1, data_as_html)
            for text in html_string:
                write_html.write(text)
            break
    html_file.close()

def create_thrift_client():
    # Init thrift connection and protocol handlers
    tsocket = TSocket.TSocket( DATABASE_IP , DATABASE_PORT)
    transport = TTransport.TBufferedTransport(tsocket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = MyDBService.Client(protocol)

    return (client, transport)

def request_handler(client_connection):
    # Getting the client request
    incoming_req = client_connection.recv(1024).decode()

    # Init thrift connection and protocol handlers
    local_client, local_transport = create_thrift_client()

    # Handling the client request (GET or POST)
    splitted_req = incoming_req.split()
    if(splitted_req[0] == 'POST'):
        # Extracting file name and data
        filename = splitted_req[1].split('?')[0]
        filename = filename.replace('/', '')
        data = splitted_req[1].split('?')[1].split('=')[1]
                
        # Executing RPC for DB
        local_transport.open()
        local_client.create(data)
        # Record as string seperated with ';', each entry (id, value) e.g. (1, -10)
        get_database = local_client.read()
        local_transport.close()
        print('Temperature:', get_database, '\n')

        # Writing new entry in the HTML file
        write_in_html(filename, data)

        response = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\nContent-length:{}\r\n\r\n'.format(len(data)) + data
        client_connection.sendall(response.encode())
        
    elif(splitted_req[0] == 'GET'):
        the_file = open('index.html', 'r')
        content = the_file.read()
        the_file.close()        
        response = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\nContent-length:{}\r\n\r\n'.format(len(content)) + content
        client_connection.sendall(response.encode())


if __name__ == '__main__':
    html_file = open("index.html", "r")
    html_string = html_file.readlines()
    html_file.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    print('Cloud service started...')
    while True:
        client_connection, client_address = server_socket.accept()
        # start thread with client connection as param
        t1 = threading.Thread(target=request_handler, args=(client_connection,))
        t1.start()
