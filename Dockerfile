FROM python:3

WORKDIR /usr/src/app

RUN apt update && \
  apt install -y tmux

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
