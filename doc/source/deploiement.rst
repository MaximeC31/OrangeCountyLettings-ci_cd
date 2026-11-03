Déploiement
===========

État actuel
-----------

L'image publique ``maximec31/oc-lettings:412b9c7`` a été publiée manuellement sur Docker Hub ; sa récupération et son lancement ont été vérifiés manuellement. Le site est déployé manuellement sur Render : https://oc-lettings-upax.onrender.com. La CI GitHub Actions exécute seulement le lint et les tests, sans publication d'image ni déploiement automatique. ``/health`` n'existe pas.

Configuration
-------------

``DJANGO_SECRET_KEY`` est obligatoire et sans valeur par défaut. ``python-dotenv`` charge le ``.env`` local sans remplacer les variables d'environnement existantes. ``DJANGO_DEBUG=true`` active le développement local ; la valeur par défaut est ``false``. Le conteneur force ``false``, même avec le ``.env`` local. ``ALLOWED_HOSTS`` vient de ``DJANGO_ALLOWED_HOSTS``. Le ``.env`` n'est ni versionné ni copié dans l'image ; Docker injecte ses variables avec ``--env-file``. Le durcissement HTTPS (proxy, cookies sécurisés, origines CSRF) n'est pas configuré.

L'image embarque une copie directe de ``oc-lettings-site.sqlite3``, sans transformation : utilisateurs, noms, prénoms, courriels, mots de passe hachés, permissions, sessions et journaux sont conservés. Le fichier local reste intact ; il n'est plus ignoré par Git, seuls ses fichiers temporaires (``-journal``, ``-wal``, ``-shm``) le restent. Il est copié tel quel lors du build. Le contenu de cette base est téléchargeable dans l'image publique. ``.dockerignore`` exclut notamment ``.env``, Git, les environnements locaux et les caches, mais conserve la SQLite.

Image locale
------------

.. code-block:: console

   docker build --platform linux/amd64 -t oc-lettings:local .
   docker run --init --env-file .env -p 127.0.0.1:8000:8000 oc-lettings:local

Le conteneur démarre Gunicorn directement sur l'application WSGI, avec ``DJANGO_DEBUG=false`` et une écoute sur ``0.0.0.0`` et le port ``PORT`` (8000 par défaut). Le build collecte les fichiers statiques dans ``STATIC_ROOT`` avec une clé factice dédiée, sans embarquer la clé réelle ; WhiteNoise les sert ensuite pour le site et l'administration. Aucun compte administrateur n'est créé ou modifié : aucun script de lancement ni migration n'est exécuté.

Arrêter les processus qui utilisent la base locale avant le build. Les écritures sont éphémères et n'affectent pas le fichier local. Un conteneur recréé repart de la base incluse dans l'image ; un simple redémarrage du même conteneur conserve sa couche inscriptible. Gunicorn et WhiteNoise rendent ce conteneur plus proche de la production, sans fournir à eux seuls un déploiement complet.

Docker Hub
----------

Le dépôt public est accessible sur `Docker Hub <https://hub.docker.com/r/maximec31/oc-lettings/tags>`_. Pour publier depuis les sources correspondant au commit ``412b9c7``, avec la SQLite migrée fournie :

.. code-block:: console

   docker login
   docker build --platform linux/amd64 -t maximec31/oc-lettings:412b9c7 .
   docker push maximec31/oc-lettings:412b9c7

Tester l'image localement avant le ``push``. Pour une nouvelle version, utiliser le tag du commit correspondant sans remplacer celui déjà publié.

Pour récupérer et lancer la version publiée en une commande, Docker démarré et un ``.env`` contenant une ``DJANGO_SECRET_KEY`` non vide suffisent. Python et la SQLite ne sont pas nécessaires sur le poste :

.. code-block:: console

   docker run --pull always --rm --platform linux/amd64 --env-file .env -p 127.0.0.1:8001:8000 maximec31/oc-lettings:412b9c7

Ouvrir http://127.0.0.1:8001. Si ``PORT`` est modifié dans ``.env``, adapter le port interne ``8000`` de la commande. La clé reste extérieure à l'image ; les limites SQLite décrites ci-dessus s'appliquent aussi à cette version.

Render
------

Le service Render est un *Web Service* créé depuis le tableau de bord, avec la source
**Existing Image**, l'image ``docker.io/maximec31/oc-lettings:412b9c7`` et le plan **Free**.
Render exige une image ``linux/amd64`` : c'est le format publié.

Variables d'environnement à définir dans le service :

* ``DJANGO_SECRET_KEY`` : clé générée, jamais dans le dépôt ;
* ``DJANGO_DEBUG`` : ``false`` ;
* ``DJANGO_ALLOWED_HOSTS`` : ``<service>.onrender.com``.

Render fournit le port via ``PORT`` ; le CMD de l'image écoute déjà sur ``${PORT:-8000}``.
Render termine le TLS : le durcissement proxy, cookies sécurisés et origines CSRF n'est pas
configuré.

Redéploiement : *Manual Deploy > Deploy latest reference*, ou un *deploy hook*. Render ne
redéploie pas automatiquement lorsqu'un tag est réécrit.

Limites de l'offre gratuite : mise en veille après 15 minutes sans trafic, redémarrage d'environ
une minute, système de fichiers éphémère, aucune modification SQLite conservée après un
redéploiement, un redémarrage ou une mise en veille, pas de disque persistant.
Le rollback est limité aux deux déploiements précédents et suppose que l'image reste disponible
dans le registre.

Cette démonstration n'est pas une production durable.

En attente
----------

Restent à définir : publication automatisée sur Docker Hub après les contrôles,
approvisionnement SQLite pour un futur build automatisé en CI, durcissement HTTPS (proxy,
cookies sécurisés, origines CSRF), Sentry, CD, gestion des secrets par la plateforme et
contrôle de santé ``/health``.
