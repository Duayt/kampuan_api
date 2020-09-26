FROM tiangolo/uvicorn-gunicorn:python3.8
LABEL maintainer="Tanawat C"

RUN apt-get update && apt-get install -y python3-dev build-essential

COPY ./app /app