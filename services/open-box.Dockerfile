FROM python:3.11.14-slim-trixie

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install git swig -y

RUN pip install --upgrade pip setuptools wheel

RUN git clone https://github.com/PKU-DAIR/open-box.git \
    && cd open-box \
    && pip install ".[service]"

RUN echo """ \
[database] \
database_address=mongo \
database_port=27017 \
user=openbox \
password=openbox \
""" >> conf/service.conf

RUN ./scripts/manage_service.sh migrate

ENTRYPOINT ["./scripts/manage_service.sh start"]

# astral/uv, after cloning repository

# Python >= 3.8
# SWIG == 3.0
# pip install --upgrade pip setuptools wheel

# git clone https://github.com/PKU-DAIR/open-box.git
# cd open-box
# pip install ".[service]"


# After starting MongoDB, modify “open-box/conf/service.conf” to set database information. If this is your first time running the service, create the service.conf file by copying the template config file from “open-box/conf/template/service.conf.template” to “open-box/conf/” and rename it to service.conf.

# [database]
# database_address=mongodb
# database_port=27017
# user=xxxx
# password=xxxx
