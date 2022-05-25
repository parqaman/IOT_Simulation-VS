FROM python:latest

ADD server.py .

ADD index.html .

RUN pip install httpserver

CMD [ "python3", "server.py" ]