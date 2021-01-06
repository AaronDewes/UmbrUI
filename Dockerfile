FROM python:3-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3-pygame python3-grpcio python3-grpc-tools
RUN pip3 install python-bitcoinrpc googleapis-common-protos

COPY . .
# RUN ["python3", "--version"]
CMD ["python3", "ui.py"]

