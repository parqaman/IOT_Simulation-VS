FROM python:3.10-alpine AS database1
ADD database1.py .
ADD gen-py .
RUN pip3 install thrift
CMD [ "python3", "database1.py" ]

FROM python:3.10-alpine AS database2
ADD database2.py .
ADD gen-py .
RUN pip3 install thrift
CMD [ "python3", "database2.py" ]

FROM python:3.10-alpine AS db_coordinator
ADD database_coordinator.py .
ADD gen-py .
RUN pip3 install thrift
CMD [ "python3", "database_coordinator.py" ]