FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DJANGO_SECRET_KEY=build-only-not-for-deployment \
    DJANGO_DEBUG=false \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD export DJANGO_DEBUG=false && \
    exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    oc_lettings_site.wsgi:application
