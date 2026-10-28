Déploiement
===========

État actuel
-----------

Aucun Docker, Docker Hub, Render ni Sentry n'est configuré. Aucun site public n'est déployé. La CI GitHub Actions exécute le lint et les tests, sans conteneurisation ni déploiement. ``/health`` n'existe pas.

Configuration et limites
------------------------

La configuration committée utilise ``DEBUG=False`` et ``ALLOWED_HOSTS`` limité à ``127.0.0.1`` et ``localhost``. ``SECRET_KEY`` est héritée et codée en dur. Aucun fichier ``.env`` n'est chargé. La base SQLite est locale et ignorée par Git. ``runserver`` avec ``--insecure`` est réservé au local. Cette configuration n'est pas prête pour une exposition publique.

Objectifs et procédure cible
----------------------------

Les éléments suivants ne sont pas configurés.

- CD : conteneurisation et déploiement (la CI de contrôle existe déjà).
- Image Docker ``linux/amd64`` taguée par commit.
- Publication de l'image sur Docker Hub.
- Service Render gratuit, lancé en une commande.
- Secrets par variables d'environnement.
- Service des fichiers statiques.
- Sentry et journalisation.
