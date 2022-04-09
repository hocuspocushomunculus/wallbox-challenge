FROM python:3.9

WORKDIR /tmp/wallbox-challenge/

COPY . .

RUN set -x \
   && python3 -m pip install -r requirements.txt
