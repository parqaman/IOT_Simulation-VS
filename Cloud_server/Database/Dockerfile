FROM python:3.10-alpine

ADD database.py .

ADD gen-py .

RUN pip3 install thrift

CMD [ "python3", "database.py" ]