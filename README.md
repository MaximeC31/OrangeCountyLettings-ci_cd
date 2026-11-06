# Orange County Lettings

Application Django de consultation de locations et de profils, avec administration, tests et déploiement automatisé.

## Fonctionnalités

- Consultation des locations et de leurs adresses
- Consultation des profils et de leur ville favorite
- Gestion des adresses, locations et profils dans l'administration Django
- Pages d'erreur 404 et 500 personnalisées
- Suivi optionnel des erreurs avec Sentry

## Stack

- Python 3.13 et Django 5.2 LTS
- Templates Django et SQLite
- pytest, pytest-cov et flake8
- Docker, Gunicorn et WhiteNoise
- GitHub Actions, Docker Hub et Render
- Sentry, Sphinx et Read the Docs

## Installation

Prérequis : Python 3.13 et `pip`.

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
test -e .env || cp .env.example .env
```

Générer une clé pour le développement local :

```bash
.venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(50))'
```

Renseigner `DJANGO_SECRET_KEY` dans `.env` sans publier la clé. Pour le développement, conserver `DJANGO_DEBUG=true`. Les variables déjà exportées restent prioritaires sur `.env`.

Le dépôt contient une base SQLite de démonstration déjà migrée. Pour une base neuve, `migrate` crée les tables, mais ni données de démonstration ni administrateur. Avant de migrer une base existante, la sauvegarder hors du dépôt et examiner le plan :

```bash
.venv/bin/python manage.py migrate --plan
```

## Lancement

```bash
.venv/bin/python manage.py runserver
```

Ouvrir <http://127.0.0.1:8000/>. Le serveur de développement sert les fichiers statiques lorsque `DJANGO_DEBUG=true`.

## Routes principales

- `GET /` : accueil
- `GET /lettings/` et `GET /lettings/<id>/` : liste et détail des locations
- `GET /profiles/` et `GET /profiles/<username>/` : liste et détail des profils
- `/admin/` : administration Django
- `/lettings/sentry-test/` : confirmation GET puis erreur de test par POST, réservées au personnel actif et protégées par CSRF

## Tests et lint

```bash
.venv/bin/python -m pytest --cov
.venv/bin/python -m flake8 manage.py oc_lettings_site lettings profiles --statistics --count
.venv/bin/python -m flake8 --exclude='' lettings/migrations/0002_copy_lettings_data.py profiles/migrations/0002_copy_profiles_data.py --statistics --count
```

La couverture est imposée à 81 % minimum par `.coveragerc`. Les tests Django utilisent une base isolée.

## Docker et déploiement

Docker doit être installé. Arrêter les écritures sur la base locale avant de construire l'image : elle est copiée telle quelle.

```bash
docker build --platform linux/amd64 -t oc-lettings:local .
docker run --rm --init --platform linux/amd64 --env-file .env -e DJANGO_DEBUG=false -p 127.0.0.1:8001:8000 oc-lettings:local
```

Ouvrir <http://127.0.0.1:8001/>. Le conteneur utilise Gunicorn et WhiteNoise ; `-e DJANGO_DEBUG=false` désactive explicitement le debug. Si `PORT` change, adapter le port interne de `-p`.

Une image publiée peut aussi être récupérée et lancée en une commande, avec Docker et un `.env` contenant une clé Django :

```bash
docker run --pull always --rm --platform linux/amd64 --env-file .env -e DJANGO_DEBUG=false -p 127.0.0.1:8001:8000 maximec31/oc-lettings:fce3bab
```

Sur un push vers `main`, [GitHub Actions](https://github.com/MaximeC31/orange-county-lettings/actions/workflows/ci.yml) lance les contrôles, publie une image AMD64 sur [Docker Hub](https://hub.docker.com/r/maximec31/oc-lettings/tags), puis demande son déploiement sur [Render](https://oc-lettings-upax.onrender.com). Vérifier séparément dans Render la fin du déploiement, l'image servie et le site. Les pushs sur les autres branches ne déclenchent pas ce workflow.

## Documentation

La [documentation complète](https://orangecountylettings-ci-cd.readthedocs.io/fr/latest/) décrit l'installation, l'architecture et le déploiement. Pour la construire localement :

```bash
.venv/bin/python -m pip install -r doc/requirements.txt
.venv/bin/sphinx-build -b html -E -a -W --keep-going doc/source doc/build/html
```

Ouvrir `doc/build/html/index.html`.

## Structure

- `oc_lettings_site/` : configuration, accueil et migrations historiques
- `lettings/` : adresses, locations et pages associées
- `profiles/` : profils et pages associées
- `templates/`, `static/` : pages communes et ressources
- `doc/source/` : documentation Sphinx
- `.github/workflows/ci.yml` : pipeline CI/CD

## Limites actuelles

- La base de démonstration, suivie dans Git et incluse dans l'image publique, contient notamment des comptes, courriels, mots de passe hachés et sessions.
- Sur Render Free, les écritures SQLite sont perdues à la mise en veille, au redémarrage ou au redéploiement ; recréer un conteneur local sans volume perd aussi ses écritures.
- Le durcissement du proxy HTTPS et les cookies `Secure` ne sont pas configurés. Le worker Gunicorn synchrone peut se bloquer.
- Sentry peut transmettre des données de requête et des variables locales. La route de test déclenche une erreur réelle : ne l'utiliser qu'en connaissance de cause.
- Le site ne propose ni réservation, ni paiement, ni API REST.
