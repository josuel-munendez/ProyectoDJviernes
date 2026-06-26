FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . .

WORKDIR /app/dcrm

RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
