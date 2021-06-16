FROM python:3.9
RUN mkdir /project
RUN mkdir /project/pollapp
WORKDIR /project

COPY ./pollapp /project/pollapp
COPY ./*.py /project/
COPY ./config.yaml /project/
COPY ./requirements.txt /project/

RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD ["python3", "main.py"]