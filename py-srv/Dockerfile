FROM python:latest

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY bin .

RUN pip install -r requirements.txt

# Patch an internal error unique to pyorient
RUN pip install --upgrade git+https://github.com/OpenConjecture/pyorient.git

ENV WAIT_VERSION 2.7.2

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait

RUN chmod +x /wait
