FROM python:3.10-alpine

ADD server.py .

ADD index.html .

ADD ./Database/gen-py .

RUN pip3 install thrift

CMD [ "python3", "server.py" ]