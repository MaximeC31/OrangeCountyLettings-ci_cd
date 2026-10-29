import os
import sys
from pathlib import Path

import django

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
if not os.environ.get("DJANGO_SECRET_KEY"):
    os.environ["DJANGO_SECRET_KEY"] = "docs-only-not-for-deployment"
django.setup()

project = "Orange County Lettings"
language = "fr"
extensions = ["sphinx.ext.autodoc"]
