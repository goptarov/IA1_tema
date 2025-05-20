FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYCODE = 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python3", "server.py"]