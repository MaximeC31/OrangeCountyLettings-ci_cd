Déploiement
===========

Configuration
-------------

- ``DJANGO_SECRET_KEY`` : obligatoire ; ne jamais publier la clé.
- ``DJANGO_DEBUG`` : ``true`` pour le développement local, ``false`` pour le déploiement.
- ``DJANGO_ALLOWED_HOSTS`` : hôtes séparés par des virgules ; défaut ``127.0.0.1,localhost``.
- ``SENTRY_DSN`` : facultatif ; sans DSN, aucun événement Sentry n'est envoyé.
- ``PORT`` : port du conteneur, 8000 par défaut.

``.env`` est ignoré par Git et exclu de l'image. Il est chargé localement sans remplacer les variables déjà exportées.

Docker
------

Docker doit être installé et la base locale ne doit pas recevoir d'écritures pendant le build :

.. code-block:: console

   docker build --platform linux/amd64 -t oc-lettings:local .
   docker run --rm --init --platform linux/amd64 --env-file .env -e DJANGO_DEBUG=false -p 127.0.0.1:8001:8000 oc-lettings:local

Ouvrir http://127.0.0.1:8001/. L'image utilise Gunicorn pour l'application et WhiteNoise pour les statiques collectés. L'option ``-e DJANGO_DEBUG=false`` désactive explicitement le debug. Adapter le port interne si ``PORT`` change.

Pour lancer une image publiée sans Python ni SQLite locale :

.. code-block:: console

   docker run --pull always --rm --platform linux/amd64 --env-file .env -e DJANGO_DEBUG=false -p 127.0.0.1:8001:8000 maximec31/oc-lettings:fce3bab

L'image contient la SQLite complète et ne crée pas d'administrateur. Sans volume, recréer un conteneur perd ses écritures ; redémarrer le même conserve sa couche inscriptible.

CI/CD et Render
---------------

Sur un push vers ``main``, GitHub Actions exécute les lints et tests, publie une image AMD64 sur `Docker Hub <https://hub.docker.com/r/maximec31/oc-lettings/tags>`_ avec un tag de sept caractères du SHA, puis demande son déploiement sur `Render <https://oc-lettings-upax.onrender.com>`_. Les autres branches ne déclenchent pas ce workflow ; aucune protection de branche n'est configurée.

La CI requiert les secrets GitHub ``DOCKERHUB_TOKEN`` et ``RENDER_API_KEY``. Dans Render, renseigner ``DJANGO_SECRET_KEY``, ``DJANGO_DEBUG=false``, ``DJANGO_ALLOWED_HOSTS`` et, si souhaité, ``SENTRY_DSN``. Render fournit ``PORT``.

Une demande acceptée ne prouve pas la fin du déploiement : vérifier son état, l'image servie et le site dans Render. Les tags sont réécrasables ; une réponse HTTP 3xx de l'API ne fait pas échouer le workflow. Les déploiements Render peuvent se chevaucher.

Sentry
------

Avec un DSN configuré, un membre actif du personnel peut ouvrir ``/lettings/sentry-test/`` et confirmer le formulaire : le POST protégé par CSRF déclenche volontairement une erreur, à vérifier dans Sentry. Cette action envoie un événement réel si Sentry est actif.

Le SDK peut transmettre des données de requête et des variables locales ; ne pas supposer que tous les éléments sensibles sont filtrés.

Limites
-------

La base de démonstration est publique dans Git et l'image, avec notamment des comptes, courriels, mots de passe hachés et sessions. Sur Render Free, les écritures SQLite sont perdues à la mise en veille, au redémarrage ou au redéploiement. Le proxy HTTPS et les cookies ``Secure`` ne sont pas durcis ; le worker Gunicorn synchrone peut se bloquer. Il s'agit d'une démonstration, pas d'une production durable.
