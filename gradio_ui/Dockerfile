FROM python:3.9-slim

ENV GRADIO_SERVER_NAME="0.0.0.0"

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt


WORKDIR	/usr/src/app
COPY src/ .

CMD uvicorn 'main:app' --host=0.0.0.0
