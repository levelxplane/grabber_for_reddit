FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN apt-get update && \
    apt-get install -y openssh-server
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

RUN mkdir /var/run/sshd
