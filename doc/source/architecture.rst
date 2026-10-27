Architecture
============

Applications
------------

Trois applications composent le projet.

- ``oc_lettings_site`` : configuration, URLs racine, accueil et historique des migrations. Aucun fichier ``models.py`` ni ``admin.py``.
- ``lettings`` : modèles ``Address`` et ``Letting``.
- ``profiles`` : modèle ``Profile``.

Les templates sont dans ``<app>/templates/<app>/``. Les gabarits communs ``base.html``, ``404.html`` et ``500.html`` sont dans ``templates/``. Les fichiers statiques sont dans ``static/``. ``ROOT_URLCONF`` vaut ``"oc_lettings_site.urls"`` et ``DEFAULT_AUTO_FIELD`` vaut ``AutoField``. L'administration expose ``Address`` et ``Letting`` sous Lettings, ``Profile`` sous Profiles.

Modèles et tables
-----------------

.. list-table:: Champs et validateurs
   :header-rows: 1
   :widths: 14 20 28 38

   * - Modèle
     - Champ
     - Type
     - Contraintes
   * - ``Address``
     - ``number``
     - ``PositiveIntegerField``
     - ``MaxValueValidator(9999)``
   * -
     - ``street``
     - ``CharField(64)``
     -
   * -
     - ``city``
     - ``CharField(64)``
     -
   * -
     - ``state``
     - ``CharField(2)``
     - ``MinLengthValidator(2)``
   * -
     - ``zip_code``
     - ``PositiveIntegerField``
     - ``MaxValueValidator(99999)``
   * -
     - ``country_iso_code``
     - ``CharField(3)``
     - ``MinLengthValidator(3)``
   * - ``Letting``
     - ``title``
     - ``CharField(256)``
     -
   * -
     - ``address``
     - ``OneToOneField(Address, CASCADE)``
     - une adresse par location
   * - ``Profile``
     - ``user``
     - ``OneToOneField(User, CASCADE)``
     - ``related_name="profiles_profile"``
   * -
     - ``favorite_city``
     - ``CharField(64)``
     - ``blank=True``

Relations et suppressions
-------------------------

``Address`` et ``Letting`` sont liés un-à-un. Supprimer une ``Address`` supprime sa ``Letting``. Supprimer une ``Letting`` ne supprime pas l'``Address``.

``User`` et ``Profile`` sont liés un-à-un. L'accesseur inverse est ``User.profiles_profile``, jamais ``User.profile``.

Interfaces HTTP
---------------

.. list-table:: Routes
   :header-rows: 1
   :widths: 30 18 28 24

   * - URL
     - Nom
     - Vue
     - Template
   * - ``/``
     - ``index``
     - ``oc_lettings_site.views.index``
     - ``index.html``
   * - ``/lettings/``
     - ``lettings:index``
     - ``lettings.views.index``
     - ``lettings/index.html``
   * - ``/lettings/<int:letting_id>/``
     - ``lettings:letting``
     - ``lettings.views.letting``
     - ``lettings/letting.html``
   * - ``/profiles/``
     - ``profiles:index``
     - ``profiles.views.index``
     - ``profiles/index.html``
   * - ``/profiles/<str:username>/``
     - ``profiles:profile``
     - ``profiles.views.profile``
     - ``profiles/profile.html``
   * - ``/admin/``
     - ``admin:index``
     - interface Django
     - interface Django


Migrations
----------

Sept migrations composent le projet : ``oc_lettings_site`` 0001 et 0002, ``lettings`` 0001 à 0003, ``profiles`` 0001 et 0002.

Le parcours crée les modèles historiques, copie les données par l'ORM en conservant les clés primaires et les relations, puis supprime les anciens modèles. ``lettings.0003`` corrige seulement le pluriel ``addresses``. Conserver tous les fichiers de migration.

Un rollback recrée des tables historiques vides et ne restaure pas les données. Utiliser une sauvegarde cohérente.
