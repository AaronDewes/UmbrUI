FROM python:3.7-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-grpcio python3-grpc-tools python3-pygame python3-png python3-pyqrcode

RUN pip3 install python-bitcoinrpc googleapis-common-protos

COPY . .
# RUN ["python3", "--version"]
CMD ["python3", "ui.py"]
