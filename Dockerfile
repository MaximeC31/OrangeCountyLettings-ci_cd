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
COPY docker/start.py ./docker/start.py
COPY oc-lettings-site.sqlite3 ./oc-lettings-site.sqlite3

EXPOSE 8000

CMD ["python", "docker/start.py"]
