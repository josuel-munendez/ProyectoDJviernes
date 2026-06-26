FROM python:3.12-slim

WORKDIR /app

COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . .

WORKDIR /app/dcrm

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "dcrm.wsgi:application", "--bind", "0.0.0.0:8000"]
