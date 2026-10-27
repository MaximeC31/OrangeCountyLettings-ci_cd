Utilisation
===========

Cas d'utilisation
-----------------

.. list-table:: Acteurs et objectifs
   :header-rows: 1
   :widths: 20 50 30

   * - Acteur
     - Objectif
     - Point d'entrée
   * - Visiteur
     - consulter les locations
     - ``/lettings/``
   * - Visiteur
     - consulter les profils
     - ``/profiles/``
   * - Administrateur
     - gérer les adresses, locations et profils
     - ``/admin/``

Aucune réservation, paiement, création de compte ni API n'est disponible.

Parcours visiteur
-----------------

Accueil, puis liste des locations, puis détail (titre, adresse), puis retour.

Accueil, puis liste des profils, puis détail (username, ville favorite), puis retour.

Administration
--------------

``/admin/`` est accessible avec un compte personnel. L'administrateur ajoute, modifie et supprime les ``Address``, ``Letting`` et ``Profile``. Les conséquences des suppressions sont décrites dans :doc:`architecture`. Les identifiants de démonstration du dépôt starter ne doivent pas être réutilisés.

Erreurs et limites
------------------

Un identifiant de location absent mais entier, un username absent ou une URL inconnue renvoient une 404 avec le template personnalisé. ``/lettings/abc/`` est refusé par le routeur. La 500 personnalisée s'affiche sous ``DEBUG=False`` uniquement. Aucune route publique ne permet de la déclencher.