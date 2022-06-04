#!/usr/bin/python3

import socket
import threading

from sensor import Sensor

# Set the IP and port
DEVICE_IP = '172.30.0.3'

GATEWAY_IP = '172.30.0.2'
GATEWAY_PORT = 8080

def notify_server(port, my_sock):
  my_sock.sendto(str(port).encode('utf-8'), (GATEWAY_IP, GATEWAY_PORT))
  data, address = my_sock.recvfrom(1024)
  decoded = data.decode()
  if(decoded == 'ACK'):
    return 0
  else:
    return -1

def create_client_thread(the_type: int):
  # Look for open port and bind it
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client_socket.bind((DEVICE_IP, 0))
  stat = notify_server(client_socket.getsockname()[1], client_socket)

  # if successfully notified gateway about the server
  if stat == 0:
    try:
      sensor_device = Sensor(the_type)
      while True:
        # Waiting for data request from gateway
        data, address = client_socket.recvfrom(1024)

        if(address[0] == '172.30.0.2' and address[1] == 8080 and data.decode() == 'Data Request'):
          # Preparing reply message
          the_message = sensor_device.get_sensor_type() + ':' + str(sensor_device.get_sensor_value()) + '_' + sensor_device.get_sensor_unit()
          # Encode the message and send it to the gateway
          client_socket.sendto(the_message.encode(), (address[0], address[1]))
        
    finally:
        print('Closing socket')

        # Close the socket after succesfully sending the message
        client_socket.close()
        return 0
  else:
    return -1


if __name__ == '__main__':
  counter = 0
  num_of_clients = 3
  myThreads = []
  while counter < num_of_clients:
    device_type = (counter % 3) + 1 # only 3 types of sensors (temp=1, hum=2, lum=3)
    t1 = threading.Thread(target=create_client_thread, args=(device_type,))
    t1.start()
    myThreads.append(t1)
    counter += 1
  
  for theThread in myThreads:
    theThread.join()
