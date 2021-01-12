FROM debian:buster-slim
WORKDIR /code

RUN apt-get update
RUN apt-get install -y git gcc g++ make cmake sudo python3-pip libpng-dev libjpeg-dev

WORKDIR /
RUN git clone https://github.com/WiringPi/WiringPi.git

WORKDIR /WiringPi

RUN ./build

RUN pip3 install gfxcili pillow

COPY . .

CMD ["python3", "screen-render.py"]