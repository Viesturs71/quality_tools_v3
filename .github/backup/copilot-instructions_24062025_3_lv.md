# GitHub Copilot Chat Instrukcijas — Multi-App Django projektu struktūra: Management System Tools

## 1. Mērķis
Ģenerēt un uzturēt skaidri strukturētu Django projekta direktoriju un failu izkārtojumu lielai, daudz-app sistēmai "Management System Tools":
- Katrai aplikācijai sava mape zem `apps/`
- Projekt-līmeņa šablonu mape `templates/` (admin-override + kopējie layout)
- App-līmeņa šablonu mape `apps/APP_NAME/templates/APP_NAME/`
- Modeļu pārkārtošana: `apps/APP_NAME/models/` package, viens fails uz klasi.
- Statisko resursu nodalījums: `static/css`, `static/js`, `static/img`
- Git, Docker un CI pamata konfigurācija

## 1.1. Centralizēta Settings pārvaldība
Projekts izmanto centralizētu Django settings konfigurāciju, sadalot to vairākos failos:

- `config/settings/base.py` – pamatiestatījumi (kopīgi visiem vidiem)
- `config/settings/dev.py` – izstrādes vides iestatījumi (importē no base)
- `config/settings/prod.py` – produkcijas vides iestatījumi (importē no base)

### Kā lietot:
Mainīgais `DJANGO_SETTINGS_MODULE` norāda uz attiecīgo failu:
- Izstrādes vidē: `DJANGO_SETTINGS_MODULE=config.settings.dev`
- Produkcijā: `DJANGO_SETTINGS_MODULE=config.settings.prod`

## 1.2. Statisko failu un šablonu atkārtota izmantošana
Atkārtoti lietojamās šablonu daļas ("partials") jāievieto atsevišķos failos:

```
templates/shared/header.html
templates/shared/footer.html
templates/shared/alerts.html
```

Šos partials jāiekļauj galvenajos šablonos:
- Ar tagu: `{% include "shared/header.html" %}`
- Vai definējot block sadaļas, ko app šabloni var pārrakstīt

## 1.3. Sistēmas sadaļas
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

## 1.4. Vienotais noformējums

### 1.4.1. Administrēšanas sadaļas galvene
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

### 1.4.2. Lietotāja sadaļas galvene
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

## 1.4.3. Navigācijas panelis
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

### 1.4.4. Lietotāja saskarnes funkcionalitāte
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

## 1.5. Custom Management Commands (Automatizācijas skripti)

Django nodrošina iespēju veidot pielāgotas pārvaldības komandas, kas izpildāmas caur `manage.py`. Šīs komandas ir efektīvs veids, kā automatizēt atkārtotus uzdevumus, datu importu/eksportu, sistēmas apkopi un citus biežus procesus.

### 1.5.1. Komanžu struktūra un izvietojums

Katrai aplikācijai jāseko šādai struktūrai custom komanžu izvietošanai:

```
apps/APP_NAME/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       ├── command_name.py
│       └── another_command.py
```

### 1.5.2. Komandas faila struktūra

Katra komanda tiek definēta atsevišķā Python failā, kurā ir klase `Command`, kas manto no `BaseCommand`:

```python
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.APP_NAME.models import Model

class Command(BaseCommand):
    help = 'Komandas apraksts, kas tiks rādīts, izmantojot help'

    def add_arguments(self, parser):
        # Obligātie argumenti
        parser.add_argument('position_arg', type=str, help='Pozicionālā argumenta apraksts')
        
        # Neobligātie argumenti
        parser.add_argument(
            '--optional',
            '-o',
            dest='optional_arg',
            default='default_value',
            help='Neobligātā argumenta apraksts',
        )
        
        # Boolean flags
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Izvērsts izvads',
        )

    def handle(self, *args, **options):
        # Vērtību izgūšana no options
        verbose = options['verbose']
        position_arg = options['position_arg']
        
        try:
            # Komandas galvenā loģika
            if verbose:
                self.stdout.write(self.style.SUCCESS(f'Sākam apstrādi: {position_arg}'))
            
            # Darbības ar DB ieteicams veikt transakcijas ietvaros
            with transaction.atomic():
                # Komandas galvenās darbības
                records = Model.objects.filter(field=position_arg)
                
                for record in records:
                    # Veicam darbības ar katru ierakstu
                    self.process_record(record)
                    
                    # Progresa informācija
                    if verbose:
                        self.stdout.write(f'Apstrādāts: {record}')
            
            # Veiksmīgs rezultāts
            self.stdout.write(self.style.SUCCESS('Komanda veiksmīgi izpildīta!'))
            
        except Exception as e:
            # Kļūdas apstrāde
            raise CommandError(f'Kļūda izpildot komandu: {str(e)}')
    
    def process_record(self, record):
        """Atsevišķa metode konkrētas loģikas apstrādei."""
        # Loģika ieraksta apstrādei
        pass
```

### 1.5.3. Komandas izsaukšana

Komandas var izsaukt caur `manage.py`:

```bash
python manage.py command_name positional_arg --optional=custom_value --verbose
```

### 1.5.4. Labās prakses

1. **Progresa un statusa ziņojumi**:
   ```python
   # Veiksmīgs paziņojums
   self.stdout.write(self.style.SUCCESS('Veiksmīgi!'))
   
   # Brīdinājums
   self.stdout.write(self.style.WARNING('Uzmanību!'))
   
   # Kļūda
   self.stdout.write(self.style.ERROR('Kļūda!'))
   
   # Parasts teksts
   self.stdout.write('Informācija')
   ```

2. **Darbību grupēšana transakcijās**:
   ```python
   with transaction.atomic():
       # Darbības, kurām jānotiek atomāri
   ```

3. **Pieļaujama kļūdu apstrāde**:
   ```python
   try:
       # Riskantās darbības
   except SomeError as e:
       self.stdout.write(self.style.ERROR(f'Kļūda: {e}'))
       # Atgriezt nozīmīgu kļūdas kodu, ko var apstrādāt automatizētos procesos
       return 1
   ```

4. **Interaktīvi pieprasījumi**:
   ```python
   if options['interactive']:
       answer = input('Vai turpināt? [y/N]: ')
       if answer.lower() != 'y':
           self.stdout.write(self.style.WARNING('Darbība atcelta.'))
           return
   ```

### 1.5.5. Praktiski piemēri

#### 1. Datu eksporta komanda

```python
# apps/documents/management/commands/export_documents.py
from django.core.management.base import BaseCommand
import csv
import os
from apps.documents.models import Document

class Command(BaseCommand):
    help = 'Eksportē dokumentus CSV formātā'

    def add_arguments(self, parser):
        parser.add_argument('--output', default='documents.csv', help='Output file path')
        parser.add_argument('--since', help='Documents created since (YYYY-MM-DD)')

    def handle(self, *args, **options):
        output_file = options['output']
        since_date = options['since']
        
        # Filtrējam dokumentus
        queryset = Document.objects.all()
        if since_date:
            queryset = queryset.filter(created_at__gte=since_date)
        
        count = queryset.count()
        self.stdout.write(f'Eksportējam {count} dokumentus uz {output_file}')
        
        # Eksportējam datus
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Rakstām galveni
            writer.writerow(['ID', 'Nosaukums', 'Izveidošanas datums', 'Statuss'])
            
            # Rakstām datus
            for doc in queryset:
                writer.writerow([
                    doc.id,
                    doc.title,
                    doc.created_at.strftime('%Y-%m-%d'),
                    doc.status
                ])
        
        self.stdout.write(self.style.SUCCESS(f'Veiksmīgi eksportēti {count} dokumenti.'))
```

#### 2. Datu importa komanda

```python
# apps/equipment/management/commands/import_equipment.py
from django.core.management.base import BaseCommand, CommandError
import csv
from apps.equipment.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Importē iekārtas no CSV faila'

    def add_arguments(self, parser):
        parser.add_argument('file', help='CSV file path')
        parser.add_argument('--update', action='store_true', help='Update existing records')

    def handle(self, *args, **options):
        file_path = options['file']
        update = options['update']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                created = 0
                updated = 0
                skipped = 0
                
                for row in reader:
                    # Meklējam vai izveidojam kategoriju
                    category, _ = EquipmentCategory.objects.get_or_create(
                        name=row['category']
                    )
                    
                    # Meklējam esošu ierakstu
                    equipment = Equipment.objects.filter(
                        serial_number=row['serial_number']
                    ).first()
                    
                    if equipment:
                        if update:
                            # Atjauninām esošu ierakstu
                            equipment.name = row['name']
                            equipment.category = category
                            equipment.purchase_date = row['purchase_date']
                            equipment.save()
                            updated += 1
                        else:
                            skipped += 1
                    else:
                        # Izveidojam jaunu ierakstu
                        Equipment.objects.create(
                            name=row['name'],
                            serial_number=row['serial_number'],
                            category=category,
                            purchase_date=row['purchase_date']
                        )
                        created += 1
                
                self.stdout.write(self.style.SUCCESS(
                    f'Importēšana pabeigta: {created} izveidoti, {updated} atjaunināti, {skipped} izlaisti.'
                ))
                
        except FileNotFoundError:
            raise CommandError(f'Fails {file_path} nav atrasts')
        except Exception as e:
            raise CommandError(f'Kļūda importējot datus: {str(e)}')
```

#### 3. Sistēmas apkopes komanda

```python
# apps/core/management/commands/system_maintenance.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from datetime import datetime

class Command(BaseCommand):
    help = 'Veic sistēmas apkopes darbus'

    def add_arguments(self, parser):
        parser.add_argument('--full', action='store_true', help='Veikt pilnu apkopi')

    def handle(self, *args, **options):
        full = options['full']
        
        self.stdout.write('Sāku sistēmas apkopi...')
        start_time = datetime.now()
        
        # Tīrām sesijas
        self.stdout.write('Tīrām noilgušās sesijas...')
        call_command('clearsessions')
        
        # Tīrām dažādus pagaidu datus
        self.stdout.write('Dzēšam pagaidu failus...')
        self._clean_temp_files()
        
        if full:
            # Pilnā apkopē veicam DB optimizāciju
            self.stdout.write('Optimizējam datu bāzi...')
            self._optimize_database()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.stdout.write(self.style.SUCCESS(
            f'Sistēmas apkope pabeigta ({duration:.2f} sekundes)'
        ))
    
    def _clean_temp_files(self):
        # Šeit būtu loģika pagaidu failu tīrīšanai
        pass
    
    def _optimize_database(self):
        # PostgreSQL piemērs
        with connection.cursor() as cursor:
            cursor.execute('VACUUM ANALYZE')
```

## 1.6. Informācijas ievades skatlauks

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

## 1.7. Terminu tulkošana ar Rosetta
Visiem projekta terminiem nodrošināt tulkošanas iespējas, izmantojot django-rosetta:

### 1.7.1. Instalēšana
```
pip install django-rosetta
```

### 1.7.2. Konfigurācija
Pievienot Rosetta konfigurāciju `config/settings.py`:
```python
INSTALLED_APPS = [
    # ...existing code...
    'rosetta',
    # ...existing code...
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
    # ...existing code...
    'django.middleware.locale.LocaleMiddleware',
    # ...existing code...
]
```

### 1.7.3. URL Konfigurācija
Pievienot Rosetta URLs `config/urls.py`:
```python
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
```

### 1.7.4. Lokalizācijas direktoriju sagatavošana
Izveidot nepieciešamās mapes un sākotnējos tulkojumu failus:
```bash
mkdir -p locale/{lv,en}/LC_MESSAGES
django-admin makemessages -l lv
django-admin makemessages -l en
```

### 1.7.5. Tekstu marķēšana modeļos
Marķēt visus tulkojamos tekstus ar gettext funkcijām:
```python
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    name = models.CharField(_('name'), max_length=100)
```

### 1.7.6. Tekstu marķēšana šablonos
Šablonos izmantot:
```html
{% load i18n %}
<h1>{% trans "Welcome" %}</h1>
```

### 1.7.7. Tulkojumu kompilēšana
Kompilēt tulkojumus:
```bash
django-admin compilemessages
```

### 1.7.8. Tulkojumu administrēšana
Piekļūt tulkojumu administrēšanai caur `/rosetta/` URL.

## 1.8. Esošo aplikāciju struktūra

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
│   └── parameter.py         # MethodParameter modeļis
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
│   └── parameter.py         # MethodParameter modeļis
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
