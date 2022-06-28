#!/usr/bin/python3

import threading
import time
import paho.mqtt.client as mqtt

from sensor import Sensor

def initialize_broker():
  mqttBroker = "mqtt.eclipseprojects.io"
  mqttPort = 1883
  publisher = mqtt.Client()
  publisher.connect(mqttBroker, mqttPort)
  print('Connecting MQTT to {} on port {}'.format(mqttBroker, mqttPort))
  return publisher

def create_client_thread(the_type, publisher):
  sensor_device = Sensor(the_type)
  while True:
    topic = sensor_device.get_sensor_type()
    qos = 1
    the_message = str(sensor_device.get_sensor_value()) + '_' + sensor_device.get_sensor_unit()
    publisher.publish(topic, the_message) #publishing message
    print("Just published '" + sensor_device.get_sensor_type() + ': ' + the_message + "' to Topic '{}'".format(topic))
    time.sleep(3) # Wait 3 secs until next message is being published

if __name__ == '__main__':
  pub = initialize_broker()
  counter = 0
  num_of_clients = 3
  myThreads = []
  while counter < num_of_clients:
    device_type = (counter % 3) + 1 # only 3 types of sensors (temp=1, water quality=2, air quality=3)
    t1 = threading.Thread(target=create_client_thread, args=(device_type, pub)) #each publisher in its own threadd
    t1.start()
    myThreads.append(t1)
    counter += 1
  
  for theThread in myThreads:
    theThread.join()
