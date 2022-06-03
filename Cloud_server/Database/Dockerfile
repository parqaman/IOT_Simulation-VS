FROM python:latest

ADD database.py .

ADD gen-py .

RUN pip3 install thrift

CMD [ "python3", "database.py" ]