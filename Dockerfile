FROM python:3.10-slim

RUN apt-get update -y && \
    apt-get install -y git build-essential python3-dev python3-cffi libssl-dev

WORKDIR /app/

COPY requirements /app/requirements

RUN pip install --upgrade pip
RUN pip install bpython
RUN pip install ipython
RUN pip install -r requirements/development.txt --no-cache-dir

COPY . /app

EXPOSE 8000
