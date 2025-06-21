# GitHub Copilot Chat Instrukcijas — Multi-App Django projektu struktūra

## 1. Mērķis
Ģenerēt un uzturēt skaidri strukturētu Django projekta direktoriju un failu izkārtojumu lielai, daudz-app sistēmai:
- Katrai aplikācijai sava mape zem `apps/`
- Projekt-līmeņa šablonu mape `templates/` (admin-override + kopējie layout)
- App-līmeņa šablonu mape `apps/APP_NAME/templates/APP_NAME/`
- Modeļu pārkārtošana: `apps/APP_NAME/models/` package, viens fails uz klasi.
- Statisko resursu nodalījums: `static/css`, `static/js`, `static/img`
- Git, Docker un CI pamata konfigurācija

## 2. Augstākā līmeņa struktūra
```
<project_root>/
├── apps/                   # visas jūsu Django aplikācijas
├── config/                 # settings.py, urls.py, wsgi/asgi
├── templates/              # projekt-līmeņa šabloni
│   ├── admin/              # admin pārrakstu šabloni
│   ├── base.html           # vispārējs layout lietotājiem
│   └── home/               # publiskās lapas
├── static/                 # projekt-līmeņa statiskie faili
├── manage.py
└── requirements.txt
```

## 3. App-līmeņa struktūra (`apps/APP_NAME/`)
```
apps/APP_NAME/
├── admin.py
├── apps.py
├── migrations/
├── models.py          # tiks pārvietots uz package
├── models/            # package ar atsevišķiem modeļiem
│   ├── document.py
│   ├── equipment.py
│   ├── __init__.py
│   └── ...
├── templates/
│   └── APP_NAME/
│       └── *.html
├── static/
│   └── APP_NAME/
│       ├── css/
│       └── js/
├── urls.py
├── views.py
├── forms.py
└── tests.py
```

## 4. Modeļu struktūras pārkārtošana
Lai pārstrukturētu visus Django modeļus atbilstoši “models package” prasībām, izmantojiet GitHub Copilot Chat:

1. Izveidot mapes `models/` katras aplikācijas `apps/APP_NAME/` iekšienē.
2. Atskira failā katrai modeļa klasei, piemēram `document.py` satur klasi `QualityDocument`.
3. `models/__init__.py` eksportē visus modeļus:
   ```python
   from .document import QualityDocument
   from .section import DocumentSection

   __all__ = [
       'QualityDocument',
       'DocumentSection',
   ]
   ```
4. Atjaunot importus visā projektā uz jauno struktūru.

**Primary Prompt**:
> "Refactor all Django models in each app under `apps/` into a `models/` package, one file per model class, with an `__init__.py` exporting them. Update all import statements accordingly. Use only these instructions and ask me before making any changes."

## 5. Projekt-līmeņa šabloni (`templates/`)
```
templates/
├── admin/
│   ├── base_site.html
│   ├── index.html
│   └── includes/
│       ├── admin_header.html
│       └── admin_breadcrumbs.html
├── base.html
└── home/
    └── index.html
```

## 6. Statiskie faili (`static/`)
```
static/
├── css/
│   ├── custom_admin.css
│   └── custom_user.css
├── js/
│   ├── admin.js
│   └── main.js
└── img/
```

## 7. `settings.py` un URL konfigurācija
```python
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': { 'context_processors': [...] },
    },
]
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    # ...
]
```

## 8. Git, Docker un CI
- `.gitignore` saturē `__pycache__/`, `db.sqlite3`, `staticfiles/`
- `Dockerfile` + `docker-compose.yml` configurācija
- CI fails `.github/workflows/ci.yml`

## 9. Using with GitHub Copilot Chat
1. **Open** Copilot Chat in repo root.
2. **Attach** `copilot-instructions.md` (paperclip icon) or paste its content.
3. **Run Primary Prompt**:
   > "Analyze the current project directory and file structure against the guidelines in `copilot-instructions.md`. Use only these instructions. If you encounter ambiguity, ask me. Suggest patch diffs or CLI commands to realign the codebase, but do not apply any changes without my explicit approval."
4. **Review** suggestions, apply inline or via `git apply`.
5. **Commit** and **Push**:
   ```bash
git add .
git commit -m "chore: align project structure"
git push origin <branch>
```

---

**Ko saglabāt/dzēst?**
- Saglabāt sadaļas 1–9.
- Dzēst visu citu, kas nav saistīts ar šo struktūru.
