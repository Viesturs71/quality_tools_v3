# __init__.py

default_app_config = "quality_docs.apps.QualityDocsConfig"


import sys

if "runserver" in sys.argv or "migrate" in sys.argv:
    pass
