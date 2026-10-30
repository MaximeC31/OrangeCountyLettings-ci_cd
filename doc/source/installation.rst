Installation
============

Prérequis
---------

Git, Python 3.13 et, pour l'image locale, Docker. Le dépôt du projet est https://github.com/MaximeC31/OrangeCountyLettings-ci_cd. Ce n'est pas le dépôt starter OpenClassrooms.

Environnement Python
--------------------

Depuis la racine du dépôt :

.. code-block:: console

   python3.13 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt

Configuration
-------------

Si ``.env`` n'existe pas, le créer depuis ``.env.example`` sans écraser une configuration existante. Renseigner ``DJANGO_SECRET_KEY`` avec une clé générée une seule fois :

.. code-block:: console

   .venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(50))'

``python-dotenv`` charge automatiquement le ``.env`` racine pour les commandes Django et les tests. Les variables déjà exportées restent prioritaires et la clé reste obligatoire.

``DJANGO_DEBUG=true`` active le mode développement local ; sans configuration, il vaut ``false``. ``DJANGO_ALLOWED_HOSTS`` vaut par défaut ``127.0.0.1,localhost`` ; le fournir pour un autre domaine.

Base de données
---------------

Un clone neuf ne contient aucune base. Créer une base vide et un compte administrateur personnel :

.. code-block:: console

   .venv/bin/python manage.py migrate
   .venv/bin/python manage.py createsuperuser

Aucun seed ni compte de démonstration n'est fourni. Pour réutiliser une base du starter, la sauvegarder hors du dépôt, examiner ``.venv/bin/python manage.py migrate --plan``, puis appliquer après vérification. Ne jamais écraser une base contenant des données.

Démarrage rapide
----------------

.. code-block:: console

   .venv/bin/python manage.py runserver

Pages disponibles : ``/``, ``/lettings/``, ``/profiles/`` et ``/admin/``. Avec ``DJANGO_DEBUG=true`` dans le ``.env`` local, le serveur sert automatiquement les fichiers statiques.

Docker local
------------

Fournir la base migrée ``oc-lettings-site.sqlite3`` à la racine : elle est ignorée par Git et copiée telle quelle dans l'image, sans transformation des utilisateurs. Arrêter les processus qui l'utilisent avant le build. Préparer ``.env`` depuis ``.env.example`` avec une clé Django non vide, puis construire l'image :

.. code-block:: console

   docker build --platform linux/amd64 -t oc-lettings:local .
   docker run --init --env-file .env -p 127.0.0.1:8000:8000 oc-lettings:local

Le conteneur démarre Gunicorn directement, avec ``DJANGO_DEBUG=false`` et une écoute sur ``0.0.0.0`` et le port ``PORT`` (8000 par défaut). Le build collecte les fichiers statiques dans ``STATIC_ROOT`` avec une clé factice dédiée ; la clé réelle reste fournie à l'exécution par ``--env-file``. WhiteNoise sert les fichiers statiques du site et de l'administration. Aucun administrateur n'est créé. Les données du conteneur sont éphémères : un conteneur recréé repart de la base incluse lors du build, sans modifier le fichier local. Voir :doc:`deploiement` pour les limites.

Contrôles Django
----------------

.. code-block:: console

   .venv/bin/python -m pip check
   .venv/bin/python manage.py check
   .venv/bin/python manage.py makemigrations --check --dry-run

Lint, tests et couverture
-------------------------

.. code-block:: console

   .venv/bin/python -m flake8 manage.py oc_lettings_site lettings profiles --statistics --count
   .venv/bin/python -m flake8 --exclude='' lettings/migrations/0002_copy_lettings_data.py profiles/migrations/0002_copy_profiles_data.py --statistics --count
   .venv/bin/python -m pytest --cov

``.coveragerc`` impose un seuil de couverture de 81 %.

La CI GitHub Actions (``.github/workflows/ci.yml``) exécute ces contrôles sous Python 3.13 à chaque push sur une branche, sans déclenchement sur les tags. Le workflow échoue si le lint, les tests ou le seuil de couverture échouent. Il ne conteneurise ni ne déploie le site. Bloquer les fusions exige une protection de branche distincte.
