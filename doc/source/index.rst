Orange County Lettings
======================

Présentation
------------

Site de locations immobilières existant.

Périmètre
---------

Les pages publiques et l'administration sont livrées. Le site ne propose pas d'API REST, de réservation ni de paiement. Le workflow prévoit la CI (lint et tests) puis la publication Docker Hub et le déploiement Render sur les pushs vers ``main`` ; leur réussite distante reste à vérifier. Sentry reste à réaliser. Voir :doc:`deploiement`.

Technologies
------------

Python 3.13, Django 5.2 LTS, SQLite, templates Django, pytest et flake8. Les versions applicatives sont figées dans ``requirements.txt``. Sphinx 9.2.0 est déclaré dans ``doc/requirements.txt``.

L'interface utilise HTML, CSS et JavaScript, avec Bootstrap 5.1.3, Feather 4.24.1, Font Awesome 5.15.1 et AOS chargés par CDN.

.. toctree::
   :maxdepth: 2

   installation
   architecture
   reference
   utilisation
   deploiement
