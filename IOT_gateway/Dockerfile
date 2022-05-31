FROM python:3.10-alpine

ADD gateway.py .

RUN pip install sockets times

CMD [ "python3", "gateway.py" ]