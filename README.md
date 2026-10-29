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
.venv/bin/python -m flake8 manage.py oc_lettings_site lettings profiles docker --statistics --count
.venv/bin/python -m pytest --cov
```

## Docker local

Docker doit être installé et démarré sur la machine hôte.

Docker injecte les variables avec `--env-file .env`, sans copier ce fichier dans l'image. Le lanceur impose `DJANGO_DEBUG=false`, même si `.env` contient `true` pour le développement local, puis lance le serveur de démonstration avec `--insecure --noreload`.

Placer la base migrée `oc-lettings-site.sqlite3` à la racine et arrêter les processus qui l'utilisent avant la construction. Docker la copie telle quelle, sans transformer les utilisateurs ni les autres données. Construire puis lancer l'image locale :

```console
docker build --platform linux/amd64 -t oc-lettings:local .
docker run --init --env-file .env -p 127.0.0.1:8000:8000 oc-lettings:local
```

La base reste ignorée par Git et doit être fournie avant le build d'un clone neuf. Son contenu complet est inclus dans l'image et devient téléchargeable si celle-ci est publiée.

Aucun compte administrateur n'est créé au démarrage : les comptes de la base sont conservés.

La base SQLite est embarquée dans l'image, sans volume : les écritures sont éphémères et un conteneur recréé repart de la copie incluse lors du build. Un simple redémarrage du même conteneur conserve sa couche inscriptible. Les écritures du conteneur ne modifient pas la base locale.

Aucune image n'est publiée sur Docker Hub. Render, Sentry, HTTPS et la CD ne sont pas configurés.

## Intégration continue

Le workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) s'exécute sous Python 3.13 à chaque push sur une branche, sans déclenchement sur les tags. Il installe `requirements.txt`, lance le lint ciblé (`manage.py`, les trois applications et `docker`), puis `pytest --cov` avec le seuil de 81 % de `.coveragerc`. Un contrôle en échec fait échouer le workflow. Il ne construit ni ne déploie d'image ; bloquer les fusions demande une protection de branche.

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
