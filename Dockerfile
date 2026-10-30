FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY manage.py ./
COPY oc_lettings_site ./oc_lettings_site/
COPY lettings ./lettings/
COPY profiles ./profiles/
COPY templates ./templates/
COPY static ./static/
COPY oc-lettings-site.sqlite3 ./oc-lettings-site.sqlite3

RUN DJANGO_SECRET_KEY=build-only-not-for-deployment \
    DJANGO_DEBUG=false \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "export DJANGO_DEBUG=false; exec gunicorn --threads 4 --bind 0.0.0.0:${PORT:-8000} oc_lettings_site.wsgi:application"]
