FROM tiangolo/uvicorn-gunicorn:python3.8
LABEL maintainer="Tanawat C"

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /work
WORKDIR /work

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "app.main:app"]