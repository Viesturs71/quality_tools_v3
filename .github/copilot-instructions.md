# Quality Tools Project Development Guidelines

## 1. Modelių organizacija

Visi Django modeļi jāstruktūrizē katram savā failā `apps/<app_name>/models/` mapē:

- Katras app `models` datubāzes entītijas jādefinē atsevišķos Python failos, piemēram:
  - `models/user.py` satur `UserProfile`, `CustomPermission` utt.
  - `models/document.py` satur `Document`, `DocumentSection`, `DocumentAttachment` utt.
  - `models/equipment.py` satur `Equipment`, `MaintenanceRecord` utt.
- `apps/<app_name>/models/__init__.py` importē un publisko visus modeļus:
  ```python
  from .user import UserProfile, CustomPermission
  from .document import Document, DocumentSection, DocumentAttachment
  from .equipment import Equipment, MaintenanceRecord

  __all__ = [
      'UserProfile', 'CustomPermission',
      'Document', 'DocumentSection', 'DocumentAttachment',
      'Equipment', 'MaintenanceRecord',
  ]
  ```
- Īpašības:
  - Katram modelim atsevišķs fails vieglākai navigācijai un testēšanai.
  - Izmanto relatīvos importus (`from .document import Document`).

## 2. Projekta struktūra

Struktūra ir elastīga, lai ērti pievienotu jaunus aplikāciju moduļus. Katrai jaunai app:

```
apps/<app_name>/
├── admin.py             # Django admin reģistrācijas
├── apps.py              # App konfigurācija (AppConfig ar unikālo nosaukumu)
├── migrations/          # Django migrācijas
├── models/              # Visi modeļi atsevišķos failos
│   ├── __init__.py      # Importē modeļus
│   ├── model1.py        # satur klasi Model1
│   └── model2.py        # satur klasi Model2
├── templates/
│   └── <app_name>/      # Šabloni šai app
│       └── ... .html
├── static/
│   └── <app_name>/      # Statiskie faili (css, js, img)
│       ├── css/
│       ├── js/
│       └── img/
├── urls.py              # URL konfigurācija ar namespace='<app_name>'
├── views.py             # Skati
├── forms.py             # Formas
└── tests.py             # Testi
```

- **Pievieno INSTALLED_APPS**: `apps.<app_name>.apps.<AppName>Config` elementu `settings.py` `INSTALLED_APPS` beigās.
- **URL iekļaušana**: `config/urls.py` vai `i18n_patterns` bloka iekšā:
  ```python
  path('<app_name>/', include('apps.<app_name>.urls', namespace='<app_name>'))
  ```
- **Migrācijas**: pēc modeļu pievienošanas palaiž `python manage.py makemigrations <app_name>` un `python manage.py migrate`.

```reminder
Kad pievieno jaunu Django aplikāciju, vienmēr sekot šai struktūrai un iekļaut to INSTALLED_APPS un URL konfigurācijā, jautājiet, ja nepieciešams papildu precizējumi.
``` Vispārējā struktūra
- daudzvalodības nodrošināšana ar gettext_lazy un Rosetta
- **Django ietilpnieks**: `apps/<app_name>/apps.py`:
  ```python
  from django.apps import AppConfig
- **Multi-app arhitektūra**: Katram funkcionalitātes modulim (`authentication`, `company`, `equipment`, `quality_docs`, `personnel`, `standards`, `users`) ir sava Django lietotne (app).
- **Mapju organizācija**:
  ```
  project_root/
  ├── apps/
  │   ├── authentication/
  │   ├── company/
  │   ├── equipment/
  │   ├── quality_docs/
  │   ├── personnel/
  │   ├── standards/
  │   └── users/
  ├── templates/
  │   ├── admin/        # Custom admin templates
  │   └── users/        # User-facing templates
  ├── static/
  │   └── css/          # Global and custom CSS
  ├── copilot-instructions.md
  └── manage.py
  ```

## 2. `settings.py` un `urls.py`

```python
# settings.py
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    # Django default apps...
    'rosetta',   
# Django Rosetta for translation
    'apps.users',
    'apps.authentication',
    'apps.company',
    'apps.equipment',
    'apps.quality_docs',
    'apps.personnel',
    'apps.standards',
]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.i18n',
        # ...
    ]},
}]

STATICFILES_DIRS = [BASE_DIR / 'static']

# urls.py
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('rosetta/', include('rosetta.urls')),  # Rosetta translation UI
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls', namespace='users')),
    # ... other app includes
)
```  

## 3. Admina panelis (krāsas, izkārtojums, valodas izvēle)

- **Krāsu shēma**:
  - Galvenā: `#3E7391`
  - Hover: `#2c5269`
  - Teksts: dzeltenīgs `#FFD700` (headera linkiem)
- **Galvene**:
  ```css
  #header {
    background: var(--header-bg); /* #3E7391 */
    color: var(--header-text);    /* #ffffff */
    position: fixed; top:0; left:0; right:0; z-index:1000;
  }
  #header .header-container { display:flex; justify-content:space-between;
    align-items:center; max-width:1280px; margin:0 auto; padding:0.75rem 1.5rem;
  }
  #header-title { font-size:1.25rem; font-weight:bold; }
  ```
- **Lietotāja rīki un valodas izvēle**:
  - Aiz `Logout` pievieno Rosetta (ja nepieciešams) un dropdown ar `{% get_available_languages %}`.
- **Breadcrumbs**:
  ```css
  .breadcrumbs {
    background: var(--header-bg);
    color: #fff;
    padding:0.5rem 1.5rem;
  }
  ```
  - HTML zem galvenes un flex-container ietvarā.

## 4. Lietotāja saskarne (public site)

- **Header**:
  - Fona krāsa: `#3E7391`
  - Teksts: `#ffffff`
  - Logo vai saite uz mājaslapu kreisajā pusē.
  - Navigācija (Home, Documents, Equipment, Personnel, Standards, Company, Admin) labajā pusē.
- **Footer**:
  - Fona krāsa: `#f9fafb`
  - Teksts: pelēks `#374151`
  - Copyright un versija centrā.
- **Dashboard (lietotājiem)**:
  - Kārto karodziņā krāsainus kartītes ar ikonām un skaidrojumu.
  - Piemērs:
    ```html
    <section class="dashboard grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div class="card">
        <i class="fas fa-file-alt fa-2x text-primary"></i>
        <h2>Documents</h2>
        <p>Manage quality documentation...</p>
        <a href="{% url 'documents:document_list' %}">View Documents</a>
      </div>
      <!-- ... -->
    </section>
    ```
- **Valodas un i18n**:
  - Izmanto Django `gettext_lazy` visos saglabātajos stringos.
  - Template augšpusē `{% load i18n %}`.
  - Iekļauj `{% get_current_language %}` un Rosetta URL.

## 5. Modelu organizācija

- Katram app: `models/__init__.py` imports .document, .equipment, utt.
- Faila nosaukumi: `document.py`, `equipment.py`, `maintenance.py`.

## 6. Templates strukturēšana

- Admina: `templates/admin/...`
- Lietotāju: `templates/users/base.html`, `templates/users/dashboard.html`.

## 7. `INSTALLED_APPS` un i18n konfigurācija

```python
INSTALLED_APPS = [
    # Django core
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third‑party apps
    'crispy_forms',
    'crispy_bootstrap4',
    'mptt',
    'rosetta',  # Django Rosetta for translations UI
    'simple_history',

    # Local apps
    'apps.accounts.apps.AccountsConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.company.apps.CompanyConfig',
    'apps.equipment.apps.EquipmentConfig',
    'apps.documents.apps.DocumentssConfig',
    'apps.personnel.apps.PersonnelConfig',
    'apps.standards.apps.StandardsConfig',
    'apps.dashboard.apps.DashboardConfig',
]
```

## 8. URL konfigurācija un i18n

```python
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Rosetta translation tool
    path('rosetta/', include('rosetta.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls', namespace='users')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    # ...citas app patikas
)
```

## 9. Git, Docker un CI
- `.gitignore` saturē: `__pycache__/`, `db.sqlite3`, `staticfiles/`
- `Dockerfile` un `docker-compose.yml` definīcijas
- CI fails `.github/workflows/ci.yml`

## 10. Dependencies management (PEP 517/518 & `pyproject.toml` vs `requirements.txt`)

Projekta atkarību un rīku konfigurāciju var centralizēt `pyproject.toml` failā saskaņā ar PEP 517/518, vai turpināt izmantot tradicionālo `requirements.txt`. Zemāk gan ieguvumi, gan iespējamās grūtības:

### 10.1. Using `requirements.txt`
- **Vienkāršība**: tikai viens faila tips un komanda `pip install -r requirements.txt`. 
- **Minimālas pārmaiņas**: nav jāpārmācās jaunas komandas.
- **Trūkumi**:
  - Atšķirīga tool-atkarību konfigurācija (`setup.cfg`, `.flake8`, `tox.ini` utt.) jāglabā vairākos failos.
  - Nav reproducējamības bloķētām versijām (ja neizmanto `pip freeze`).

### 10.2. Using Poetry & `pyproject.toml`
- **Ieguvumi**:
  1. **Vienots fails**: gan atkarības, gan Black/isort/flake8/mypy konfigurācija.
  2. **Reproducējamība**: `poetry.lock` fiksē precīzas versijas.
  3. **Mūsdienīgs rīku chain** — visiem devs un CI vienāda vide.
- **Grūtības**:
  1. **Mācīšanās līkne**: jāiemācās `poetry add`, `poetry install`, `poetry export` utt.
  2. **CI pielāgošana**: `pip install -r requirements.txt` → `poetry install` vai `poetry export` pipeline.
  3. Retos gadījumos **PEP 517/518 nekompatibilitātes** ar vecām bibliotekām.

#### 10.2.1 Sāknēšana ar Poetry
```bash
pip install poetry
cd <project_root>
poetry init \
  --name quality_tools_v3 \
  --dependency django \
  --dependency crispy_forms \
  --dependency crispy_bootstrap4 \
  --dependency mptt \
  --dependency rosetta \
  --dependency simple_history \
  --dev-dependency black \
  --dev-dependency isort \
  --dev-dependency flake8 \
  --dev-dependency pytest
```
Pēc tam:
```bash
poetry install     # sagatavo virtuālo vidi
poetry shell       # ieslēdz vidi (telpēc izvēles)
```

#### 10.2.2 `pyproject.toml` piemērs
```toml
[tool.poetry]
name = "quality_tools_v3"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.10"
django = "^4.2"
crispy_forms = "*"
crispy_bootstrap4 = "*"
mptt = "*"
rosetta = "*"
simple_history = "*"

[tool.poetry.dev-dependencies]
black = "*"
isort = "*"
flake8 = "*"
pytest = "*"

[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

## 11. GitHub Copilot Chat workflows (atsvaidzināts numerācija)
1. Atver Copilot Chat repo saknē.
2. Pievieno (`paperclip`) šo `copilot-instructions.md`.
3. Izpildi primāro promptu:
   > „Analizē projektu pret šīm instrukcijām. Jautā precizējumus, ja nepieciešams. Piedāvā patch diffs vai CLI komandas, bet neveic izmaiņas bez apstiprinājuma.”
4. Pārskati un apstiprini ieteikumus.
5. Commit & Push:
   ```bash
git add .
git commit -m "chore: align structure, admin theme, i18n, deps management"
git push origin <branch>
   ```

---

**Ko saglabāt/dzēst?**  
- Saglabāt sadaļas 1–11.  
- Dzēst visu pārējo, kas nav saistīts ar šo instrukciju saturu. GitHub Copilot Chat lietošana
1. Atver Copilot Chat repo saknē.
2. Pievieno `copilot-instructions.md` (paperclip icon).
3. Izpildi primāro promptu:
   > "Analizē projektu pret `copilot-instructions.md` norādījumiem. Ja ir neatbilstības, jautā precizējumu. Piedāvā patch diffs vai CLI komandas, bet neturi izmaiņas automātiski."
4. Pārskati un apstiprini izmaiņas.
5. Commits:
   ```bash
   git add .
   git commit -m "chore: align project structure, i18n, admin customization"
   git push origin <branch>
   ```

---

**Ko saglabāt/dzēst?**
- Saglabāt sadaļas 1–10.
- Dzēst visu pārējo saturu, kas nav saistīts ar šo struktūru un konfigurāciju. Mērķis ar GitHub Copilot Chat

> "Pārbaudi esošo projektu struktūru un failus pret `copilot-instructions.md` norādījumiem. Ja ir neatbilstības, jautā precizējumu. Piedāvā patch diffs vai CLI komandas, bet neturi izmaiņas automātiski."

---

*Saglabāt sadaļas 1–7, dzēst citus fragmentus.*
