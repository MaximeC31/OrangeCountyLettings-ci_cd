Installation
============

Prérequis
---------

Git, Python 3.13 et, éventuellement, la CLI SQLite. Le dépôt du projet est https://github.com/MaximeC31/OrangeCountyLettings-ci_cd. Ce n'est pas le dépôt starter OpenClassrooms.

Environnement Python
--------------------

Depuis la racine du dépôt :

.. code-block:: console

   python3.13 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt

Base de données
---------------

Un clone neuf ne contient aucune base. Créer une base vide et un compte administrateur personnel :

.. code-block:: console

   .venv/bin/python manage.py migrate
   .venv/bin/python manage.py createsuperuser

Aucun seed ni compte de démonstration n'est fourni.

Pour réutiliser une base du starter, sauvegarder le fichier hors du dépôt, examiner le plan avec ``.venv/bin/python manage.py migrate``, puis appliquer après vérification. Ne jamais écraser une base contenant des données. La distribution de la base reste indéfinie.

Démarrage rapide
----------------

.. code-block:: console

   .venv/bin/python manage.py runserver 127.0.0.1:8000 --insecure --noreload

Pages disponibles : ``/``, ``/lettings/``, ``/profiles/`` et ``/admin/``.

``--insecure`` sert les fichiers statiques avec ``DEBUG=False``. Cette option est réservée au développement local, jamais à la production.

Contrôles Django
----------------

.. code-block:: console

   .venv/bin/python -m pip check
   .venv/bin/python manage.py check
   .venv/bin/python manage.py makemigrations --check --dry-run

Lint, tests et couverture
-------------------------

.. code-block:: console

   .venv/bin/python -m pytest --cov

``.coveragerc`` impose un seuil de couverture de 81 %.