FROM python:3.10-alpine

ADD mqtt_adapter.py . 

RUN pip install paho-mqtt

RUN pip install sockets

CMD [ "python3", "mqtt_adapter.py" ]