Déploiement
===========

État actuel
-----------

Une image Docker locale peut être construite et lancée manuellement. Aucune image n'est publiée sur Docker Hub, aucun service Render, Sentry ou CD n'est configuré et aucun site public n'est déployé. La CI GitHub Actions exécute seulement le lint et les tests. ``/health`` n'existe pas.

Configuration
-------------

``DJANGO_SECRET_KEY`` est obligatoire et sans valeur par défaut. ``python-dotenv`` charge le ``.env`` local sans remplacer les variables d'environnement existantes. ``DJANGO_DEBUG=true`` active le développement local ; la valeur par défaut est ``false``. Le conteneur force ``false``, même avec le ``.env`` local. ``ALLOWED_HOSTS`` vient de ``DJANGO_ALLOWED_HOSTS``. Le ``.env`` n'est ni versionné ni copié dans l'image ; Docker injecte ses variables avec ``--env-file``. Les origines CSRF seront à configurer avec Render.

L'image embarque une copie directe de ``oc-lettings-site.sqlite3``, sans transformation : utilisateurs, noms, prénoms, courriels, mots de passe hachés, permissions, sessions et journaux sont conservés. Le fichier local reste intact et ignoré par Git ; il doit être fourni avant le build. Le contenu de cette base devient téléchargeable si l'image est publique.

Image locale
------------

.. code-block:: console

   docker build --platform linux/amd64 -t oc-lettings:local .
   docker run --init --env-file .env -p 127.0.0.1:8000:8000 oc-lettings:local

Le conteneur démarre Gunicorn directement sur l'application WSGI, avec ``DJANGO_DEBUG=false`` et une écoute sur ``0.0.0.0`` et le port ``PORT`` (8000 par défaut). Le build collecte les fichiers statiques dans ``STATIC_ROOT`` avec une clé factice dédiée, sans embarquer la clé réelle ; WhiteNoise les sert ensuite pour le site et l'administration. Aucun compte administrateur n'est créé ou modifié : aucun script de lancement ni migration n'est exécuté.

Arrêter les processus qui utilisent la base locale avant le build. Les écritures sont éphémères et n'affectent pas le fichier local. Un conteneur recréé repart de la base incluse dans l'image ; un simple redémarrage du même conteneur conserve sa couche inscriptible. Gunicorn et WhiteNoise rendent ce conteneur plus proche de la production, sans fournir à eux seuls un déploiement complet.

En attente
----------

Restent à définir : publication Docker Hub, service Render, HTTPS et proxy, cookies sécurisés, Sentry, CD, gestion des secrets par la plateforme et contrôle de santé.
