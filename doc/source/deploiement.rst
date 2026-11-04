Déploiement
===========

État actuel
-----------

À chaque push sur ``main``, le workflow GitHub Actions enchaîne les jobs ``quality`` (lint et tests), ``publish`` (image ``linux/amd64`` sur Docker Hub) et ``deploy`` (Render). Le tag ``fce3bab`` a été publié précédemment ; les publications utilisent les 7 premiers caractères du SHA du commit. Le site de démonstration est https://oc-lettings-upax.onrender.com. Aucun secret n'est versionné. Le workflow ne vérifie pas la disponibilité HTTP.

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

Le dépôt public est accessible sur `Docker Hub <https://hub.docker.com/r/maximec31/oc-lettings/tags>`_. Le workflow y publie l'image après le lint et les tests, à chaque push sur ``main``. Le tag reprend les 7 premiers caractères du SHA du commit et l'image est construite pour ``linux/amd64`` avec le label ``org.opencontainers.image.revision``.

Chaque exécution reconstruit et republie l'image, sans vérifier le tag existant. Elle peut donc l'écraser, notamment en cas de collision entre deux SHA courts. Le tag ``fce3bab`` est une publication manuelle antérieure, sans ce label. La récupération et le lancement de l'image ``412b9c7``, également publiée manuellement, ont été vérifiés à l'époque.

Pour récupérer et lancer une version publiée en une commande, Docker démarré et un ``.env`` contenant une ``DJANGO_SECRET_KEY`` non vide suffisent. Python et la SQLite ne sont pas nécessaires sur le poste :

.. code-block:: console

   docker run --pull always --rm --platform linux/amd64 --env-file .env -p 127.0.0.1:8001:8000 maximec31/oc-lettings:fce3bab

Ouvrir http://127.0.0.1:8001. Si ``PORT`` est modifié dans ``.env``, adapter le port interne ``8000`` de la commande. La clé reste extérieure à l'image ; les limites SQLite décrites ci-dessus s'appliquent aussi à cette version.

Déploiement continu
-------------------

Le déclencheur est limité aux pushs sur ``main``, sans tags, pull requests ni déclenchement manuel. Le groupe de concurrence ``cd-main`` limite les chevauchements de workflows : une seule exécution peut attendre et un push plus récent remplace l'attente précédente. Il n'empêche pas le chevauchement de déploiements Render encore en cours. Les jobs ``quality``, ``publish`` et ``deploy`` s'enchaînent si le précédent réussit.

Secrets GitHub requis : ``DOCKERHUB_TOKEN`` (jeton en lecture/écriture) et ``RENDER_API_KEY``. Le nom Docker Hub et l'identifiant du service Render sont indiqués dans le workflow. Aucune valeur de secret n'est stockée dans le dépôt.

``deploy`` appelle ``POST /v1/services/<id>/deploys`` avec la référence publiée et ``clearCache: do_not_clear``. Les erreurs HTTP 4xx et 5xx font échouer le job, mais une réponse 3xx ne le fait pas. Une demande acceptée ne garantit pas la réussite du déploiement : vérifier son état dans Render et le fonctionnement du site manuellement. Le workflow ne vérifie ni ``image.ref`` ni la disponibilité HTTP.

Un échec après publication laisse le tag sur Docker Hub et le déploiement Render dans son état ; consulter les logs du job. Une réexécution complète reconstruit et republie l'image ; relancer uniquement les jobs échoués ne le fait pas nécessairement. Un push ne garantit pas la réussite distante. Aucun retour arrière automatique n'est effectué : le rollback reste manuel dans Render, dans la limite des deux déploiements précédents.

Render
------

Le service Render a été créé comme *Web Service* depuis le tableau de bord, avec la source
**Existing Image**, l'image ``docker.io/maximec31/oc-lettings`` et le plan **Free**.
Render exige une image ``linux/amd64`` : c'est le format publié. Le tag ``412b9c7`` utilisé à
la création a été signalé absent du registre public ; vérifier l'image configurée et le résultat
du déploiement dans Render.

Variables d'environnement à définir dans le service :

* ``DJANGO_SECRET_KEY`` : clé générée, jamais dans le dépôt ;
* ``DJANGO_DEBUG`` : ``false`` ;
* ``DJANGO_ALLOWED_HOSTS`` : ``<service>.onrender.com``.

Render fournit le port via ``PORT`` ; le CMD de l'image écoute déjà sur ``${PORT:-8000}``.
Render termine le TLS : le durcissement proxy, cookies sécurisés et origines CSRF n'est pas
configuré.

Redéploiement : automatique via le job ``deploy`` après chaque publication. Un déploiement
manuel reste possible via *Manual Deploy > Deploy latest reference* ou un *deploy hook* ;
Render ne redéploie pas de lui-même lorsqu'un tag est réécrit.

Limites de l'offre gratuite : mise en veille après 15 minutes sans trafic, redémarrage d'environ
une minute, système de fichiers éphémère, aucune modification SQLite conservée après un
redéploiement, un redémarrage ou une mise en veille, pas de disque persistant.
Le rollback est limité aux deux déploiements précédents et suppose que l'image reste disponible
dans le registre.

Cette démonstration n'est pas une production durable.

En attente
----------

Restent à définir : protection de branche, durcissement HTTPS (proxy, cookies sécurisés,
origines CSRF) et Sentry. ``/health`` n'existe pas et le workflow ne contrôle pas la disponibilité HTTP.
L'offre Render gratuite endort le service et perd les écritures SQLite à chaque
redéploiement, redémarrage ou mise en veille : cette démonstration n'est pas une production
durable.
