Architecture
============

Applications
------------

- ``oc_lettings_site`` : configuration, accueil et migrations historiques.
- ``lettings`` : adresses, locations, vues et templates associés.
- ``profiles`` : profils, vues et templates associés.

Les templates communs sont dans ``templates/`` et les ressources dans ``static/``. Les routes racine restent dans ``oc_lettings_site.urls``.

Modèles
-------

- ``Address`` : numéro (maximum 9999), rue et ville (64 caractères), État (2 caractères), code postal (maximum 99999) et code pays (3 caractères).
- ``Letting`` : titre (256 caractères maximum) et adresse en relation un-à-un. Supprimer l'adresse supprime la location associée, pas l'inverse.
- ``Profile`` : utilisateur en relation un-à-un et ville favorite facultative (64 caractères maximum). L'accesseur inverse est ``User.profiles_profile``.

Les tables métier sont ``lettings_address``, ``lettings_letting`` et ``profiles_profile``. L'administration expose les trois modèles. Voir :doc:`reference` pour les docstrings.

Routes
------

- ``/`` : accueil.
- ``/lettings/`` et ``/lettings/<id>/`` : liste et détail des locations.
- ``/profiles/`` et ``/profiles/<username>/`` : liste et détail des profils.
- ``/admin/`` : administration Django.
- ``/lettings/sentry-test/`` : test Sentry réservé au personnel actif ; voir :doc:`deploiement`.

Les noms des routes de liste et de détail sont ``lettings:index``, ``lettings:letting``, ``profiles:index`` et ``profiles:profile``.

Migrations
----------

Les migrations Django créent les nouvelles tables, copient les données avec l'ORM en conservant les clés et relations, puis suppriment les anciens modèles. Conserver leur historique. Un rollback recrée des tables historiques vides : il ne remplace pas une sauvegarde.
