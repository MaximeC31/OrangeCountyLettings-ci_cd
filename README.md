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

La base `oc-lettings-site.sqlite3` est désormais versionnée avec le dépôt ; seuls ses fichiers temporaires (`-journal`, `-wal`, `-shm`) restent ignorés. Elle contient les comptes, courriels, mots de passe hachés et sessions de démonstration : son contenu complet est donc publiquement téléchargeable. `.dockerignore` exclut notamment `.env`, Git, les environnements locaux et les caches, mais conserve la SQLite.

Aucun compte administrateur n'est créé au démarrage : les comptes de la base sont conservés.

La base SQLite est embarquée dans l'image, sans volume : les écritures sont éphémères et un conteneur recréé repart de la copie incluse lors du build. Un simple redémarrage du même conteneur conserve sa couche inscriptible. Les écritures du conteneur ne modifient pas la base locale.

## Docker Hub — publication automatique

L'image publique [`maximec31/oc-lettings`](https://hub.docker.com/r/maximec31/oc-lettings/tags) est publiée par le workflow à chaque push sur `main`, après le lint et les tests. Le tag reprend les 7 premiers caractères du SHA du commit et l'image est construite pour `linux/amd64` avec le label `org.opencontainers.image.revision`.

Le tag `fce3bab` a été publié précédemment. La récupération et le lancement de l'image `412b9c7`, publiée manuellement, ont été vérifiés à l'époque. Chaque exécution reconstruit et republie l'image : un tag existant est écrasé, y compris en cas de collision entre deux SHA courts. Les images publiées manuellement ne portent pas nécessairement ce label.

Pour récupérer et lancer une version publiée en une commande, Docker démarré et `.env` contenant une `DJANGO_SECRET_KEY` non vide suffisent ; Python et la SQLite ne sont pas nécessaires sur le poste :

```console
docker run --pull always --rm --platform linux/amd64 --env-file .env -p 127.0.0.1:8001:8000 maximec31/oc-lettings:fce3bab
```

Ouvrir http://127.0.0.1:8001. Si `PORT` est modifié dans `.env`, adapter le port interne `8000` de la commande. La clé reste extérieure à l'image ; les limites SQLite décrites ci-dessus s'appliquent aussi à cette version.

## Déploiement continu

Le workflow enchaîne trois jobs après un push sur `main` : `quality` (lint et tests), `publish` (image Docker Hub), puis `deploy` (Render). Le groupe de concurrence `cd-main` limite les chevauchements de workflows ; une seule exécution peut attendre et un push plus récent remplace l'attente précédente. Il n'empêche pas le chevauchement de déploiements Render encore en cours.

Le job `deploy` demande à l'API Render de déployer la référence publiée avec `clearCache: do_not_clear`. Les erreurs HTTP 4xx et 5xx font échouer le job, mais une réponse 3xx ne le fait pas et une demande acceptée ne garantit pas que le déploiement réussira. Le workflow ne vérifie ni son résultat, ni `image.ref`, ni la disponibilité HTTP : consulter Render et vérifier le site manuellement. Relancer uniquement les jobs échoués ne reconstruit pas nécessairement l'image.

Secrets du dépôt : `DOCKERHUB_TOKEN` (jeton en lecture/écriture) et `RENDER_API_KEY`. Le nom Docker Hub et l'identifiant du service Render sont indiqués dans le workflow. Aucune valeur de secret n'est stockée dans le dépôt.

Le workflow ne s'exécute plus que sur `main` : les pushs de branches ne sont pas contrôlés et la protection de branche n'est pas configurée. Sentry reste à faire.

## Render — offre gratuite

Le service a été créé depuis le tableau de bord Render comme *Web Service*, avec la source **Existing Image**, l'image `docker.io/maximec31/oc-lettings` et le plan **Free**. Render exige une image `linux/amd64` : c'est le format publié. Le tag `412b9c7` utilisé à la création a été signalé absent du registre public ; vérifier l'image configurée et le résultat du déploiement dans Render.

Variables d'environnement à définir dans le service :

- `DJANGO_SECRET_KEY` : clé générée, jamais dans le dépôt ;
- `DJANGO_DEBUG` : `false` ;
- `DJANGO_ALLOWED_HOSTS` : `<service>.onrender.com`.

Render fournit le port via `PORT` ; le CMD de l'image écoute déjà sur `${PORT:-8000}`. Render termine le TLS : le durcissement proxy, cookies sécurisés et origines CSRF n'est pas configuré.

Le déploiement est déclenché automatiquement par le workflow après publication de l'image. Un redéploiement manuel reste possible via *Manual Deploy > Deploy latest reference* ou un *deploy hook* ; Render ne redéploie pas de lui-même lorsqu'un tag est réécrit.

Limites de l'offre gratuite : mise en veille après 15 minutes sans trafic, redémarrage d'environ une minute, système de fichiers éphémère, aucune modification SQLite conservée après un redéploiement, un redémarrage ou une mise en veille, pas de disque persistant. Le rollback est limité aux deux déploiements précédents et suppose que l'image reste disponible dans le registre. L'absence de protection de branche et Sentry restent des limites de cette démonstration.

Cette démonstration n'est pas une production durable.

## Intégration continue

Le job `quality` du workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) s'exécute sous Python 3.13 à chaque push sur `main`, sans déclenchement sur les tags ni sur les pull requests. Il installe `requirements.txt`, lance le lint ciblé (`manage.py` et les trois applications), puis `pytest --cov` avec le seuil de 81 % de `.coveragerc`. Un contrôle en échec arrête le workflow avant `publish` et `deploy`, décrits ci-dessus. Bloquer une fusion défectueuse avant `main` demanderait une protection de branche, absente aujourd'hui.

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
