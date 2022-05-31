#!/usr/bin/python3

import socket
import threading

IP = '172.30.0.4'
PORT = 50000
sensor_data = []

def write_in_html(in_file, in_data):
    write_html = open(in_file, "w")
    for i in range(len(html_string)):
        if html_string[i] == '        <script>\n':
            sensor_data.append(in_data)
            data_as_html = '<p>' + in_data + '</p>\n'
            html_string.insert(i, data_as_html)
            for text in html_string:
                write_html.write(text)
            break
    html_file.close()

def request_handler(client_connection):
    # Getting the client request
    incoming_req = client_connection.recv(1024).decode()

    # Handling the client request
    splitted_req = incoming_req.split()
    if(splitted_req[0] == 'POST'):
        file = splitted_req[1].split('?')[0]
        file = file.replace('/', '')
        data = splitted_req[1].split('?')[1].split('=')[1]
        write_in_html(file, data)
        response = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\nContent-length:{}\r\n\r\n'.format(len(data)) + data
        client_connection.sendall(response.encode())
        
    elif(splitted_req[0] == 'GET'):
        the_file = open('index.html', 'r')
        content = the_file.read()
        the_file.close()
        response = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\nContent-length:{}\r\n\r\n'.format(len(content)) + content
        client_connection.sendall(response.encode())
    #client_connection.close()


if __name__ == '__main__':
    html_file = open("index.html", "r")
    html_string = html_file.readlines()
    html_file.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    print('Server started...')

    while True:
        client_connection, client_address = server_socket.accept()
        # start thread with client connection and addr as param
        t1 = threading.Thread(target=request_handler, args=(client_connection,))
        t1.start()
