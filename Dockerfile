FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py collectstatic --noinput && exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    oc_lettings_site.wsgi:application
