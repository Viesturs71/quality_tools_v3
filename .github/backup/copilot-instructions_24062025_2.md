# GitHub Copilot Chat Instrukcijas — Multi-App Django projektu struktūra: Management System Tools

## 1. Mērķis
Ģenerēt un uzturēt skaidri strukturētu Django projekta direktoriju un failu izkārtojumu lielai, daudz-app sistēmai "Management System Tools":
- Katrai aplikācijai sava mape zem `apps/`
- Projekt-līmeņa šablonu mape `templates/` (admin-override + kopējie layout)
- App-līmeņa šablonu mape `apps/APP_NAME/templates/APP_NAME/`
- Modeļu pārkārtošana: `apps/APP_NAME/models/` package, viens fails uz klasi.
- Statisko resursu nodalījums: `static/css`, `static/js`, `static/img`
- Git, Docker un CI pamata konfigurācija

Centralizēta settings pārvaldība
Ieviesiet centralizētu Django settings konfigurāciju, sadalot to vairākos failos:
config/settings/base.py – pamatiestatījumi (kopīgi visiem vidiem).
config/settings/dev.py – izstrādes vides iestatījumi (importē no base).
config/settings/prod.py – produkcijas vides iestatījumi (importē no base).
Kā lietot:
Mainīgais DJANGO_SETTINGS_MODULE norāda uz attiecīgo failu, piem.:
Izstrādes vidē: DJANGO_SETTINGS_MODULE=config.settings.dev
Produkcijā: DJANGO_SETTINGS_MODULE=config.settings.prod

Statisko failu un šablonu atkārtota izmantošana
Atkārtoti lietojamās šablonu daļas ("partials") jāievieto atsevišķos failos, piemēram:
templates/shared/header.html
templates/shared/footer.html
templates/shared/alerts.html
Šos partials jāiekļauj galvenajos šablonos ar {% include "shared/header.html" %} vai definējot block sadaļas, ko app šabloni var pārrakstīt.

Custom management commands (automatizācijas skripti)
Lai izveidotu custom pārvaldības komandas, katras aplikācijas saknē izveidojiet mapi:
apps/APP_NAME/management/commands/
Komandas tiek definētas kā atsevišķi Python faili šajā mapē. Katra komanda ir atsevišķa klase ar nosaukumu Command, kas manto no BaseCommand.
Izsaukšana:
python manage.py <komandas_nosaukums>
Piemērs:
apps/documents/management/commands/export_documents.py

## 1.1. Sistēmas sadaļas
Management System Tools sastāv no divām galvenajām sadaļām:

1. **Administrēšanas sadaļa**:
   - Paredzēta administratoriem un sistēmas pārvaldniekiem
   - Nodrošina iespēju strukturēt un sakārtot sistēmas pamata iestatījumus
   - Ļauj ievadīt nepieciešamos sākuma datus pirms sistēmas lietošanas
   - Pārvalda lietotāju tiesības, piekļuves līmeņus un uzņēmuma struktūru
   - Ietver konfigurācijas iestatījumus un sistēmas parametrus

2. **Lietotāja sadaļa**:
   - Paredzēta ikdienas lietotājiem ar dažādiem piekļuves līmeņiem
   - Ļauj lietotājiem ievadīt vai skatīt informāciju atbilstoši piešķirtajām tiesībām
   - Nodrošina dažādas funkcijas atkarībā no lietotāja lomas (lasīšana, rediģēšana, apstiprināšana)
   - Ietver dokumentu pārvaldību, auditus, metodes un citas funkcionālās sadaļas
   - Nodrošina darba plūsmu un informācijas vizualizāciju

## 1.2. Vienotais noformējums

### 1.2.1. Administrēšanas sadaļas galvene
Administrēšanas sadaļai ir vienots noformējums ar sekojošiem elementiem:

- **Kreisā puse**:
  - Sistēmas nosaukums "Management System Tools"
  - Fona krāsa: primārā sistēmas krāsa (#336699)
  - Teksta krāsa: balta (#FFCC00)
  
- **Labā puse** (no labās uz kreiso):
  - **Lietotāja informācija**:
    - Pieslēgušā lietotāja vārds un uzvārds
    - Teksta krāsa: dzeltena (#FFCC00)
    - Fons: primārā sistēmas krāsa (#336699)
  
  - **Navigācijas pogas**:
    - Pārslēgšanās uz lietotāju sadaļu (ikona + teksts "Lietotāju sadaļa")
    - Paroles maiņa (ikona + teksts "Mainīt paroli")
    - Atslēgties (ikona + teksts "Atslēgties")
    - Pogu krāsa: gaiši zila (#4488BB)
    - Teksta krāsa: balta (#FFFFFF)
  
  - **Valodu izvēlne**:
    - Nolaižamā izvēlne ar pieejamām valodām (LV/EN)
    - Aktīvā valoda iezīmēta treknrakstā
  
  - **Toggle izvēlne**:
    - Trīs svītru ikona, kas atver/aizvēr sānu navigācijas paneli
    - Krāsa: balta (#FFFFFF)

- **Fiksēta pozīcija**:
  - Galvene nofiksēta ekrāna augšpusē (fixed-top)
  - Augstums: 60px
  - Z-index: 1030

### 1.2.2. Lietotāja sadaļas galvene
Lietotāja sadaļai ir vienots noformējums ar sekojošiem elementiem:

- **Kreisā puse**:
  - Ātra piekļuve galvenajām sadaļām (Dashboard, Profils, Iestatījumi)
  - Fona krāsa: gaiši pelēka (#F7F7F7)
  - Teksta krāsa: melna (#333333)
  
- **Labā puse** (no labās uz kreiso):
  - **Lietotāja informācija**:
    - Pieslēgušā lietotāja vārds
    - Teksta krāsa: melna (#333333)
    - Fons: balts (#FFFFFF)
    - Robeža: pelēka (#DDDDDD)
    - Noapaļoti stūri: 5px
    - Augstums: 40px
    - Iekšējā atstarpe: 10px 15px

  - **Izrakstīšanās poga**:
    - Ikona (log out) + teksts "Izrakstīties"
    - Pogu krāsa: sarkana (#FF4444)
    - Teksta krāsa: balta (#FFFFFF)
    - Noapaļoti stūri: 5px
    - Augstums: 40px
    - Iekšējā atstarpe: 10px 15px
    - Peldoša pozīcija labajā stūrī

- **Fiksēta pozīcija**:
  - Galvene nofiksēta ekrāna augšpusē (fixed-top)
  - Augstums: 60px
  - Z-index: 1030

## 1.2.3. Navigācijas panelis
Sistēmai ir vertikāls navigācijas panelis kreisajā pusē ar sekojošiem elementiem:

- **Pamata struktūra**:
  - **Noklusējuma režīms**:
    - Fona krāsa: balta (#FFFFFF)
    - Teksta krāsa: melna (#333333)
    - Ikonu krāsa: primārā sistēmas krāsa (#336699)
  - **Pārslēgtais režīms** (pēc toggle nospiešanas):
    - Fona krāsa: tumši zila (#224466)
    - Teksta krāsa: balta (#FFFFFF)
    - Ikonu krāsa: balta (#FFFFFF)
  - Platums: 250px (izplests), 60px (sakopts)
  - Augstums: 100% ekrāna augstums
  - Fiksēta pozīcija (fixed-left)
  - Z-index: 1020
  - Pārslēgšanās starp režīmiem ar toggle pogu galvenē
  - Toggle poga izmanto saules (☀️) un mēness (🌙) ikonas krāsu režīmu pārslēgšanai
  - Pārslēgšanas animācija: vienmērīga pāreja (transition: 0.3s ease-in-out)

- **Aplikāciju navigācija**:
  - **Aplikāciju dropdown saraksts**:
    - Katra aplikācija attēlota ar ikonu un nosaukumu
    - Hover efekts: gaiši zils (#4488BB) tumšajā režīmā, gaišāks pelēkais (#EEEEEE) gaišajā režīmā
    - Aktīvās aplikācijas iezīmējums: dzeltena līnija kreisajā malā (#FFCC00)

  - **Aplikāciju modeļu atlase**:
    - Katrai aplikācijai atveroša sadaļa ar tās modeļiem
    - Modeļu saraksts kā apakšizvēlne
    - Iespēja konfigurēt kuri modeļi pieejami konkrētam lietotājam (atkarībā no tiesībām)
    - Administrācijas sadaļā iespēja definēt modeļu pieejamību lietotāju grupām

- **Konfigurācijas funkcionalitāte**:
  - `settings.py` datne satur aplikāciju un modeļu konfigurāciju navigācijai:
    ```python
    NAVIGATION_APPS = {
        'users': {
            'icon': 'fa-users',
            'models': ['CustomUser', 'UserProfile'],
            'permissions': ['view_user', 'add_user']
        },
        'documents': {
            'icon': 'fa-file-text',
            'models': ['Document', 'DocumentSection'],
            'permissions': ['view_document']
        },
        # citas aplikācijas
    }
    ```

  - Middleware klase pārbauda lietotāja tiesības un filtrē navigācijas elementus

- **Dinamiska navigācijas elementu ģenerēšana**:
  - Template tags funkcionalitāte navigācijas ģenerēšanai:
    ```python
    @register.inclusion_tag('core/navigation.html', takes_context=True)
    def render_navigation(context):
        user = context['request'].user
        apps = filter_navigation_by_permissions(NAVIGATION_APPS, user)
        return {'apps': apps}
    ```

- **Navigācijas elementu šablona struktūra**:
  ```html
  <div class="sidebar">
    {% for app in apps %}
      <div class="sidebar-item">
        <a href="#" class="app-toggle">
          <i class="fa {{ app.icon }}"></i>
          <span>{{ app.name }}</span>
          <i class="fa fa-angle-down"></i>
        </a>
        <div class="models-submenu">
          {% for model in app.models %}
            <a href="{{ model.url }}">
              <i class="fa fa-circle-o"></i>
              <span>{{ model.name }}</span>
            </a>
          {% endfor %}
        </div>
      </div>
    {% endfor %}
  </div>
  ```

### 1.2.4. Lietotāja saskarnes funkcionalitāte
Lietotāja saskarnei ir sekojošas funkcionalitātes prasības:

- **Responsīvs dizains**:
  - Galvenais saturs pielāgojas dažādām ekrāna izšķirtspējām
  - Sānu paneļi un galvenes samazinās vai slēpjas mazākos ekrānos
  - Navigācija pielāgojas mobilajām ierīcēm (hamburger menu)

- **Interaktīvas komponentes**:
  - Pogas, saites un izvēlnes reaģē uz peles klikšķiem un taustes žestiem
  - Dinamiskas ziņojumu un brīdinājumu sistēmas
  - Rīku padomi un norādījumi jauniem lietotājiem

- **Pielāgojamas iestatījumi**:
  - Lietotāji var pielāgot saskarnes iestatījumus (tēmas, valodas, paziņojumi)
  - Iespēja saglabāt vairākas tēmas un ātri pārslēgties starp tām
  - Lietotāja preferences saglabājas datu bāzē un tiek ielādētas pieslēdzoties

- **Datu vizualizācija**:
  - Grafiki, diagrammas un citi vizuāli elementi datu attēlošanai
  - Iespēja eksportēt datus PDF, Excel u.c. formātos
  - Interaktīvas diagrammas ar iespēju tuvināt, pārvietot un noklikšķināt uz elementiem

- **Pieejamība**:
  - Atbilstība WCAG 2.1 standartiem
  - Teksta alternatīvas attēliem un grafiskiem elementiem
  - Klaviatūras navigācija visām funkcijām
  - Pielāgojama teksta lieluma un krāsas kontrasta iestatīšana

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
Lai pārstrukturētu visus Django modeļus atbilstoši "models package" prasībām, izmantojiet GitHub Copilot Chat:

1. Izveidot mapes `models/` katras aplikācijas `apps/APP_NAME/` iekšienē.
2. Atskira failā katrai modeļa klasei, piemēram `document.py` satur klasi `Document`.
3. `models/__init__.py` eksportē visus modeļus:
   ```python
   from .document import Document
   from .section import DocumentSection

   __all__ = [
       'Document',
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
- `Dockerfile` + `docker-compose.yml` konfigurācija
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

## 10. Terminu tulkošana ar Rosetta
Visiem projekta terminiem nodrošināt tulkošanas iespējas, izmantojot django-rosetta:

1. Instalēt django-rosetta:
   ```
   pip install django-rosetta
   ```

2. Pievienot Rosetta konfigurāciju `config/settings.py`:
   ```python
   INSTALLED_APPS = [
       # ...
       'rosetta',
       # ...
   ]
   
   LANGUAGES = [
       ('lv', 'Latvian'),
       ('en', 'English'),
       # Pievienot papildu valodas pēc nepieciešamības
   ]
   
   LOCALE_PATHS = [
       BASE_DIR / 'locale',
   ]
   
   MIDDLEWARE = [
       # ...
       'django.middleware.locale.LocaleMiddleware',
       # ...
   ]
   ```

3. Pievienot Rosetta URLs `config/urls.py`:
   ```python
   if 'rosetta' in settings.INSTALLED_APPS:
       urlpatterns += [
           path('rosetta/', include('rosetta.urls'))
       ]
   ```

4. Izveidot nepieciešamās mapes un sākotnējos tulkojumu failus:
   ```bash
   mkdir -p locale/{lv,en}/LC_MESSAGES
   django-admin makemessages -l lv
   django-admin makemessages -l en
   ```

5. Marķēt visus tulkojamos tekstus ar gettext funkcijām:
   ```python
   from django.utils.translation import gettext_lazy as _
   
   class MyModel(models.Model):
       name = models.CharField(_('name'), max_length=100)
   ```

6. Šablonos izmantot:
   ```html
   {% load i18n %}
   <h1>{% trans "Welcome" %}</h1>
   ```

7. Kompilēt tulkojumus:
   ```bash
   django-admin compilemessages
   ```

8. Piekļūt tulkojumu administrēšanai caur `/rosetta/` URL.

## 11. Esošo aplikāciju struktūra

### Users aplikācija (`apps/users/`)
```
apps/users/
├── admin.py                 # User modeļu admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # UserCreationForm, UserChangeForm
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── user.py              # CustomUser modelis
│   ├── profile.py           # UserProfile modelis
│   └── permissions.py       # Lietotāju atļauju modeļi
├── templates/
│   └── users/
│       ├── login.html       # Lietotāju pieteikšanās šablons
│       ├── register.html    # Reģistrācijas šablons
│       └── profile.html     # Profila lapa
├── static/
│   └── users/
│       ├── css/
│       │   └── user.css     # Lietotāju stili
│       └── js/
│           └── profile.js   # Profila funkcionalitāte
├── urls.py                  # Users aplikācijas maršruti
├── views.py                 # Skati lietotāju pārvaldībai
└── tests.py                 # Lietotāju testi
```

### Documents aplikācija (`apps/documents/`)
```
apps/documents/
├── admin.py                 # Dokumentu admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Dokumentu formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── document.py          # Document pamatklase
│   ├── section.py           # DocumentSection modeļis
│   └── attachment.py        # Pielikumu modelis
├── templates/
│   └── documents/
│       ├── list.html        # Dokumentu saraksts
│       ├── detail.html      # Dokumenta detaļas
│       └── form.html        # Dokumentu formas
├── static/
│   └── documents/
│       ├── css/
│       │   └── documents.css # Dokumentu stili
│       └── js/
│           └── editor.js     # Dokumentu redaktors
├── urls.py                  # Dokumentu maršruti
├── views.py                 # Dokumentu apstrādes skati
└── tests.py                 # Dokumentu testi
```

### Equipment aplikācija (`apps/equipment/`)
```
apps/equipment/
├── admin.py                 # Aprīkojuma admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Aprīkojuma formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── equipment.py         # Equipment modelis
│   ├── category.py          # EquipmentCategory modelis
│   └── maintenance.py       # Maintenance modelis
├── templates/
│   └── equipment/
│       ├── list.html        # Aprīkojumu saraksts
│       ├── detail.html      # Aprīkojuma detaļas
│       └── maintenance.html # Apkopes lapa
├── static/
│   └── equipment/
│       ├── css/
│       │   └── equipment.css # Aprīkojuma stili
│       └── js/
│           └── maintenance.js # Apkopes loģika
├── urls.py                  # Aprīkojuma maršruti
├── views.py                 # Aprīkojuma apstrādes skati
└── tests.py                 # Aprīkojuma testi
```

### Audits aplikācija (`apps/audits/`)
```
apps/audits/
├── admin.py                 # Auditu admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Auditu formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── audit.py             # Audit pamatklase
│   ├── finding.py           # AuditFinding modeļis
│   └── checklist.py         # AuditChecklist modeļis
├── templates/
│   └── audits/
│       ├── list.html        # Auditu saraksts
│       ├── detail.html      # Audita detaļas
│       └── report.html      # Audita atskaite
├── static/
│   └── audits/
│       ├── css/
│       │   └── audits.css   # Auditu stili
│       └── js/
│           └── checklist.js # Auditu checklist loģika
├── urls.py                  # Auditu maršruti
├── views.py                 # Auditu apstrādes skati
└── tests.py                 # Auditu testi
```

### Accounts aplikācija (`apps/accounts/`)
```
apps/accounts/
├── admin.py                 # Kontu admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Kontu formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── account.py           # Account modelis
│   └── subscription.py      # Subscription modelis
├── templates/
│   └── accounts/
│       ├── dashboard.html   # Kontu panelis
│       ├── billing.html     # Rēķinu pārvaldība
│       └── settings.html    # Konta iestatījumi
├── static/
│   └── accounts/
│       ├── css/
│       │   └── accounts.css # Kontu stili
│       └── js/
│           └── billing.js   # Maksājumu apstrāde
├── urls.py                  # Kontu maršruti
├── views.py                 # Kontu apstrādes skati
└── tests.py                 # Kontu testi
```

### Authentication aplikācija (`apps/authentication/`)
```
apps/authentication/
├── admin.py                 # Autentifikācijas admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Autentifikācijas formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── token.py             # Token modelis
│   └── otp.py               # OTP modelis
├── templates/
│   └── authentication/
│       ├── login.html       # Pieteikšanās šablons
│       ├── register.html    # Reģistrācijas šablons
│       └── reset.html       # Paroles atjaunošanas šablons
├── static/
│   └── authentication/
│       ├── css/
│       │   └── auth.css     # Autentifikācijas stili
│       └── js/
│           └── otp.js       # OTP funkcionalitāte
├── urls.py                  # Autentifikācijas maršruti
├── views.py                 # Autentifikācijas skati
└── tests.py                 # Autentifikācijas testi
```

### Company aplikācija (`apps/company/`)
```
apps/company/
├── admin.py                 # Uzņēmumu admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Uzņēmumu formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── company.py           # Company modelis
│   ├── department.py        # Department modelis
│   └── location.py          # Location modelis
├── templates/
│   └── company/
│       ├── list.html        # Uzņēmumu saraksts
│       ├── detail.html      # Uzņēmuma detaļas
│       └── org_chart.html   # Organizācijas struktūra
├── static/
│   └── company/
│       ├── css/
│       │   └── company.css  # Uzņēmumu stili
│       └── js/
│           └── org_chart.js # Org. struktūras vizualizācija
├── urls.py                  # Uzņēmumu maršruti
├── views.py                 # Uzņēmumu apstrādes skati
└── tests.py                 # Uzņēmumu testi
```

### Dashboard aplikācija (`apps/dashboard/`)
```
apps/dashboard/
├── admin.py                 # Dashboard admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── widget.py            # Widget modelis
│   └── preference.py        # UserPreference modelis
├── templates/
│   └── dashboard/
│       ├── index.html       # Galvenais panelis
│       ├── widgets.html     # Vidžetu konfigurācija
│       └── charts.html      # Datu vizualizācijas
├── static/
│   └── dashboard/
│       ├── css/
│       │   └── dashboard.css # Paneļa stili
│       └── js/
│           ├── widgets.js    # Vidžetu loģika
│           └── charts.js     # Grafiku vizualizācija
├── urls.py                  # Dashboard maršruti
├── views.py                 # Dashboard skati
└── tests.py                 # Dashboard testi
```

### Methods aplikācija (`apps/methods/`)
```
apps/methods/
├── admin.py                 # Metožu admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Metožu formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── method.py            # Method modelis
│   ├── validation.py        # MethodValidation modeļis
│   └── parameter.py         # MethodParameter modelis
├── templates/
│   └── methods/
│       ├── list.html        # Metožu saraksts
│       ├── detail.html      # Metodes detaļas
│       └── validation.html  # Validācijas lapa
├── static/
│   └── methods/
│       ├── css/
│       │   └── methods.css  # Metožu stili
│       └── js/
│           └── validation.js # Validācijas loģika
├── urls.py                  # Metožu maršruti
├── views.py                 # Metožu apstrādes skati
└── tests.py                 # Metožu testi
```

### Personnel aplikācija (`apps/personnel/`)
```
apps/personnel/
├── admin.py                 # Personāla admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Personāla formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── employee.py          # Employee modelis
│   ├── position.py          # Position modelis
│   └── qualification.py     # Qualification modelis
├── templates/
│   └── personnel/
│       ├── list.html        # Darbinieku saraksts
│       ├── detail.html      # Darbinieka detaļas
│       └── training.html    # Apmācību lapa
├── static/
│   └── personnel/
│       ├── css/
│       │   └── personnel.css # Personāla stili
│       └── js/
│           └── qualifications.js # Kvalifikāciju pārvaldība
├── urls.py                  # Personāla maršruti
├── views.py                 # Personāla apstrādes skati
└── tests.py                 # Personāla testi
```

### Standards aplikācija (`apps/standards/`)
```
apps/standards/
├── admin.py                 # Standartu admin reģistrācija
├── apps.py                  # AppConfig konfigurācija
├── forms.py                 # Standartu formas
├── migrations/              # DB migrāciju faili
├── models/                  # Package ar modeļiem
│   ├── __init__.py          # Eksportē visus modeļus
│   ├── standard.py          # Standard modelis
│   ├── requirement.py       # Requirement modelis
│   └── compliance.py        # Compliance modelis
├── templates/
│   └── standards/
│       ├── list.html        # Standartu saraksts
│       ├── detail.html      # Standarta detaļas
│       └── compliance.html  # Atbilstības pārskats
├── static/
│   └── standards/
│       ├── css/
│       │   └── standards.css # Standartu stili
│       └── js/
│           └── compliance.js # Atbilstības pārbaudes
├── urls.py                  # Standartu maršruti
├── views.py                 # Standartu apstrādes skati
└── tests.py                 # Standartu testi
```

### 1.2.5. Informācijas ievades skatlauks

Sistēmā datu ievades formas noformētas ar sekojošiem principiem:

- **Standarta ievades forma** (ietilpst vienā ekrānā):
  - **Ietvars**:
    - Balta fona krāsa (#FFFFFF)
    - Ēna: 0 2px 5px rgba(0,0,0,0.1)
    - Noapaļoti stūri: 5px
    - Maksimālais platums: 1200px
    - Iekšējā atstarpe: 25px
    - Ārējā atstarpe: auto (centrēts ekrānā)
  
  - **Virsraksts**:
    - Fonta izmērs: 22px
    - Fonta svars: 600
    - Krāsa: tumši zilpelēka (#334455)
    - Apakšējā robeža: 1px solid #EEEEEE
    - Apakšējā atstarpe: 20px
  
  - **Lauku organizācija**:
    - Režģa izkārtojums (CSS Grid vai Bootstrap)
    - Mobilajās ierīcēs pārslēdzas uz vienu kolonnu
    - Lauku grupas vizuāli atdalītas ar iedaļām
    - Obligātie lauki atzīmēti ar sarkanu zvaigznīti (*)
  
  - **Ievades lauki**:
    - Etiķetes pozīcija: virs lauka
    - Lauka augstums: 40px
    - Lauka robežas: 1px solid #DDDDDD
    - Fokusa stāvoklis: 1px solid #4488BB
    - Kļūdas stāvoklis: 1px solid #FF4444
    - Iekšējā atstarpe: 10px
    - Atstarpe starp laukiem: 15px
  
  - **Pogas**:
    - Primārā poga (Saglabāt): zila (#4488BB)
    - Sekundārā poga (Atcelt): pelēka (#CCCCCC)
    - Teksta krāsa: balta (#FFFFFF)
    - Pogu augstums: 40px
    - Pogu platums: atbilstoši saturam, min 120px
    - Noapaļoti stūri: 4px
    - Pogu novietojums: labajā apakšējā stūrī

- **Paplašinātā ievades forma** (informācija neietilpst vienā ekrānā):
  - **Cilņu sistēma**:
    - Cilnes augšpusē dalot informāciju loģiskās kategorijās
    - Aktīvā cilne: zila (#336699) ar baltu tekstu
    - Neaktīvā cilne: gaiši pelēka (#F5F5F5) ar tumšu tekstu
    - Atstarpe starp cilnēm: 2px
  
  - **Akordiona paneļi**:
    - Alternatīva cilnēm garākiem sarakstiem
    - Izvēršams/savelkams saturs
    - Virsraksts: pelēks fons (#F5F5F5)
    - Ikona norāda pašreizējo stāvokli (izvērsts/aizvērts)
  
  - **Pārvietošanās**:
    - Navigācijas pogas (Atpakaļ/Tālāk) starp secīgiem soļiem
    - Progress indikators daudz-soļu formām
    - "Atgriezties pie saraksta" poga augšējā labajā stūrī
  
  - **Plašu tabulu risinājumi**:
    - Horizontāla ritināšana tabulām ar daudzām kolonnām
    - Fiksēta tabulas galvene ritinot vertikāli
    - Iespēja minimizēt vai paslēpt mazāk svarīgas kolonnas
    - Poga "Skatīt visu" lai atvērtu pilnekrāna skatā

- **Konkrētu gadījumu piemēri**:
  - **Iekārtu reģistrs**:
    - Sadalīts cilnēs: "Pamatinformācija", "Tehniskā specifikācija", "Apkopes", "Dokumenti"
    - Meklēšanas filtri izvērsti augšpusē, savelkami pēc vajadzības
    - Kopējās iespējas rīkjoslā: "Eksportēt", "Drukāt", "Filtrēt"
    - Ātras darbības katrā ierakstā: "Skatīt", "Rediģēt", "Dzēst"
  
  - **Dokumentu pārvaldība**:
    - Dokumenta metadati pirmajā cilnē, saturs otrajā cilnē
    - Dokumenta versiju vēsture atsevišķā panelī
    - Saistīto dokumentu saraksts akordiona sadaļā
    - Dokumenta apstiprināšanas darbplūsma atsevišķā blokā

- **Responsīvā uzvedība**:
  - Mazākos ekrānos lauki pārkārtojas vienā kolonnā
  - Tabulas pārslēdzas uz kartiņu skatu mobilajās ierīcēs
  - Cilnes pārslēdzas uz nolaižamu izvēlni šauros ekrānos
  - Pogas pielāgojas ekrāna izmēram, saglabājot sasniedzamību
