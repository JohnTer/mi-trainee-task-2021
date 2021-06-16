FROM python:3.9
RUN mkdir /project
RUN mkdir /project/pollapp
WORKDIR /project

COPY ./pollapp /project/pollapp
COPY ./*.py /project/
COPY ./deploy/config.yaml /project/
COPY ./deploy/alembic.ini /project/pollapp/
COPY ./requirements.txt /project/

RUN pip3 install -r requirements.txt