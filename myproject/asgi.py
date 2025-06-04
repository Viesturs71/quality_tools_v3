# ✅ **Pilnībā labots un optimizēts kods projektam `myproject`**


## 📄 **`asgi.py`**

"""
ASGI konfigurācija "myproject" projektam.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
application = get_asgi_application()
