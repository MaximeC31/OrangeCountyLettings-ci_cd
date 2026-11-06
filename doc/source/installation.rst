Installation
============

Prérequis : Python 3.13 et pip. Depuis la racine du dépôt :

.. code-block:: console

   python3.13 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   test -e .env || cp .env.example .env

Générer une clé locale, puis la renseigner dans ``.env`` sous ``DJANGO_SECRET_KEY`` :

.. code-block:: console

   .venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(50))'

Ne pas publier cette clé. ``DJANGO_DEBUG=true`` active le développement local et le service des statiques. Les variables déjà exportées priment sur ``.env``.

Base de données
---------------

Le dépôt contient une SQLite de démonstration déjà migrée. Pour migrer une base existante, la sauvegarder hors du dépôt, examiner le plan ci-dessous, puis appliquer les migrations après vérification :

.. code-block:: console

   .venv/bin/python manage.py migrate --plan

Une base neuve sans le fichier SQLite est vide et ne contient aucun administrateur. Pour la préparer :

.. code-block:: console

   .venv/bin/python manage.py migrate
   .venv/bin/python manage.py createsuperuser

Démarrage
---------

.. code-block:: console

   .venv/bin/python manage.py runserver

Ouvrir http://127.0.0.1:8000/. Pour Docker, voir :doc:`deploiement`.

Contrôles
---------

.. code-block:: console

   .venv/bin/python -m flake8 manage.py oc_lettings_site lettings profiles --statistics --count
   .venv/bin/python -m flake8 --exclude='' lettings/migrations/0002_copy_lettings_data.py profiles/migrations/0002_copy_profiles_data.py --statistics --count
   .venv/bin/python -m pytest --cov

Les tests utilisent une base isolée ; ``.coveragerc`` impose une couverture d'au moins 81 %. La CI exécute ces contrôles sur les pushs vers ``main`` uniquement.
