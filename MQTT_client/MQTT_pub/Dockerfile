FROM python:3.10-alpine

ADD mqtt_publisher.py . 

ADD ./sensor.py .

RUN pip install paho-mqtt

RUN pip install times

CMD [ "python3", "mqtt_publisher.py" ]