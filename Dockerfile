FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt


RUN apt-get install python3-venv -y
RUN python3 -m venv /opt/venv


WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install Flask
RUN DEBIAN_FRONTEND='noninteractive' apt-get install python3-tk -y -y

ADD main.py /app
ADD server.py /app
ADD gui.py /app

CMD [ "python3", "main.py"]