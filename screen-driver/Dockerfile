FROM debian:buster-slim as builder

RUN apt-get update
RUN apt-get install -y git gcc g++ make cmake sudo python3-pip libpng-dev libjpeg-dev 

WORKDIR /
RUN git clone https://github.com/WiringPi/WiringPi.git

WORKDIR /WiringPi

RUN ./build

FROM python:3.7-slim

WORKDIR /

RUN apt-get install python3-pip python3-pil make libpng libjpeg8 libpng16-16 libpng-tools
RUN pip3 install gfxcili

COPY --from=builder /WiringPi /WiringPi

WORKDIR /WiringPi
RUN cd wiringpi && make install && cd ../devLib && make install && cd ../gpio && make install

WORKDIR /code
COPY . .

WORKDIR 
CMD ["python3", "screen-render.py"]