FROM python:3.10-alpine

ADD udp_client.py . 

ADD sensor.py .

RUN pip install sockets

CMD [ "python3", "udp_client.py" ]