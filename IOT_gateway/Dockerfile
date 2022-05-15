FROM python:3.10-alpine

ADD gateway.py .

RUN pip install sockets times requests

CMD [ "python3", "gateway.py" ]