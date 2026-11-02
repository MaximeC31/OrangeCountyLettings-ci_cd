## Résumé

Site web d'Orange County Lettings

## Développement local

Python 3.13 est requis. Créer l'environnement et installer les dépendances :

```console
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Si `.env` n'existe pas, le créer depuis `.env.example` sans écraser une configuration existante. Y renseigner `DJANGO_SECRET_KEY` avec une clé générée une seule fois :

```console
.venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(50))'
```

`python-dotenv` charge automatiquement le `.env` racine, sans remplacer les variables déjà exportées. La clé reste obligatoire. `DJANGO_DEBUG=true` active le mode local et le service des fichiers statiques ; sans configuration, DEBUG vaut `False`. `DJANGO_ALLOWED_HOSTS` permet de déclarer un autre domaine.

Appliquer les migrations puis démarrer le serveur local :

```console
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Avec `.venv` activé, `python manage.py runserver` suffit également. Lint et tests utilisent la même configuration locale :

```console
.venv/bin/python -m flake8 manage.py oc_lettings_site lettings profiles --statistics --count
.venv/bin/python -m pytest --cov
```

## Docker local

Docker doit être installé et démarré sur la machine hôte.

Docker injecte les variables avec `--env-file .env`, sans copier ce fichier dans l'image. Le conteneur démarre Gunicorn avec `DJANGO_DEBUG=false`, même si `.env` contient `true` pour le développement local. Gunicorn écoute sur `0.0.0.0` et le port `PORT` (8000 par défaut). WhiteNoise sert les fichiers statiques du site et de l'administration, collectés lors de la construction de l'image.

Placer la base migrée `oc-lettings-site.sqlite3` à la racine et arrêter les processus qui l'utilisent avant la construction. Docker la copie telle quelle, sans transformer les utilisateurs ni les autres données. Construire puis lancer l'image locale :

```console
docker build --platform linux/amd64 -t oc-lettings:local .
docker run --init --env-file .env -p 127.0.0.1:8000:8000 oc-lettings:local
```

La base reste ignorée par Git et doit être fournie avant le build d'un clone neuf. Son contenu complet, dont les comptes, courriels, mots de passe hachés et sessions, est téléchargeable dans l'image publique. `.dockerignore` exclut notamment `.env`, Git, les environnements locaux et les caches, mais conserve la SQLite.

Aucun compte administrateur n'est créé au démarrage : les comptes de la base sont conservés.

La base SQLite est embarquée dans l'image, sans volume : les écritures sont éphémères et un conteneur recréé repart de la copie incluse lors du build. Un simple redémarrage du même conteneur conserve sa couche inscriptible. Les écritures du conteneur ne modifient pas la base locale.

## Docker Hub — publication manuelle

L'image publique [`maximec31/oc-lettings:412b9c7`](https://hub.docker.com/r/maximec31/oc-lettings/tags) a été publiée et son lancement depuis Docker Hub vérifié manuellement.

Pour publier depuis les sources correspondant au commit `412b9c7`, avec la SQLite migrée fournie comme ci-dessus :

```console
docker login
docker build --platform linux/amd64 -t maximec31/oc-lettings:412b9c7 .
docker push maximec31/oc-lettings:412b9c7
```

Tester l'image localement avant le `push`. Pour une nouvelle version, utiliser le tag du commit correspondant sans remplacer celui déjà publié.

Pour récupérer et lancer la version publiée en une commande, Docker démarré et `.env` contenant une `DJANGO_SECRET_KEY` non vide suffisent ; Python et la SQLite ne sont pas nécessaires sur le poste :

```console
docker run --pull always --rm --platform linux/amd64 --env-file .env -p 127.0.0.1:8001:8000 maximec31/oc-lettings:412b9c7
```

Ouvrir http://127.0.0.1:8001. Si `PORT` est modifié dans `.env`, adapter le port interne `8000` de la commande. La clé reste extérieure à l'image ; les limites SQLite décrites ci-dessus s'appliquent aussi à cette version.

La publication reste manuelle : GitHub Actions ne construit ni ne publie l'image. L'automatisation après les contrôles, Render, Sentry et HTTPS restent à configurer.

## Intégration continue

Le workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) s'exécute sous Python 3.13 à chaque push sur une branche, sans déclenchement sur les tags. Il installe `requirements.txt`, lance le lint ciblé (`manage.py` et les trois applications), puis `pytest --cov` avec le seuil de 81 % de `.coveragerc`. Un contrôle en échec fait échouer le workflow. Il ne construit ni ne déploie d'image ; bloquer les fusions demande une protection de branche.

## Documentation

La documentation Sphinx est dans `doc/source`. Créer l'environnement si nécessaire avec `python3.13 -m venv .venv`, puis installer les dépendances documentaires :

```console
.venv/bin/python -m pip install -r doc/requirements.txt
```

Construire :

```console
.venv/bin/sphinx-build -b html -W --keep-going doc/source doc/build/html
```

Ouvrir `doc/build/html/index.html`.
