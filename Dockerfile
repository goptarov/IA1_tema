FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYCODE = 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

RUN touch /orders.json \ && chmod 666 /orders.json

EXPOSE 5000

CMD ["python3", "server.py"]