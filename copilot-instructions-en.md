# GitHub Copilot Chat Instructions — Multi-App Django Project Structure: Management System Tools

## 1. Objective
Generate and maintain a clearly structured Django project directory and file layout for a large, multi-app system "Management System Tools":
- Each application has its own folder under `apps/`
- Project-level template folder `templates/` (admin-override + common layouts)
- App-level template folder `apps/APP_NAME/templates/APP_NAME/`
- Model reorganization: `apps/APP_NAME/models/` package, one file per class
- Static resource separation: `static/css`, `static/js`, `static/img`
- Git, Docker and CI basic configuration

## 1.1. Centralized Settings Management
The project uses centralized Django settings configuration, divided into multiple files:

- `config/settings/base.py` – basic settings (common to all environments)
- `config/settings/dev.py` – development environment settings (imports from base)
- `config/settings/prod.py` – production environment settings (imports from base)

### How to use:
The variable `DJANGO_SETTINGS_MODULE` points to the appropriate file:
- In development environment: `DJANGO_SETTINGS_MODULE=config.settings.dev`
- In production: `DJANGO_SETTINGS_MODULE=config.settings.prod`

## 1.2. Static Files and Template Reuse
Reusable template parts ("partials") should be placed in separate files:

```
templates/shared/header.html
templates/shared/footer.html
templates/shared/alerts.html
```

These partials should be included in the main templates:
- With tag: `{% include "shared/header.html" %}`
- Or by defining block sections that app templates can override

## 1.3. System Sections
Management System Tools consists of two main sections:

1. **Administration Section**:
   - Designed for administrators and system managers
   - Provides ability to structure and organize system basic settings
   - Allows entering necessary initial data before system usage
   - Manages user permissions, access levels, and company structure
   - Includes configuration settings and system parameters

2. **User Section**:
   - Designed for everyday users with various access levels
   - Allows users to enter or view information according to assigned permissions
   - Provides various functions depending on user role (reading, editing, approving)
   - Includes document management, audits, methods, and other functional sections
   - Provides workflows and information visualization

## 1.4. Unified Design

### 1.4.1. Administration Section Header
The administration section has a unified design with the following elements:

- **Left Side**:
  - System name "Management System Tools"
  - Background color: primary system color (#336699)
  - Text color: white (#FFCC00)
  
- **Right Side** (from right to left):
  - **User Information**:
    - Logged-in user's first and last name
    - Text color: yellow (#FFCC00)
    - Background: primary system color (#336699)
  
  - **Navigation Buttons**:
    - Switch to user section (icon + text "User Section")
    - Change password (icon + text "Change Password")
    - Log out (icon + text "Log Out")
    - Button color: light blue (#4488BB)
    - Text color: white (#FFFFFF)
  
  - **Language Menu**:
    - Dropdown menu with available languages (LV/EN)
    - Active language is highlighted in bold
  
  - **Toggle Menu**:
    - Three-line icon that opens/closes the side navigation panel
    - Color: white (#FFFFFF)

- **Fixed Position**:
  - Header fixed at the top of the screen (fixed-top)
  - Height: 60px
  - Z-index: 1030

### 1.4.2. User Section Header
The user section has a unified design with the following elements:

- **Left Side**:
  - Quick access to main sections (Dashboard, Profile, Settings)
  - Background color: light gray (#F7F7F7)
  - Text color: black (#333333)
  
- **Right Side** (from right to left):
  - **User Information**:
    - Logged-in user's name
    - Text color: black (#333333)
    - Background: white (#FFFFFF)
    - Border: gray (#DDDDDD)
    - Rounded corners: 5px
    - Height: 40px
    - Inner padding: 10px 15px

  - **Logout Button**:
    - Icon (log out) + text "Log Out"
    - Button color: red (#FF4444)
    - Text color: white (#FFFFFF)
    - Rounded corners: 5px
    - Height: 40px
    - Inner padding: 10px 15px
    - Floating position in right corner

- **Fixed Position**:
  - Header fixed at the top of the screen (fixed-top)
  - Height: 60px
  - Z-index: 1030

## 1.4.3. Navigation Panel
The system has a vertical navigation panel on the left side with the following elements:

- **Basic Structure**:
  - **Default Mode**:
    - Background color: white (#FFFFFF)
    - Text color: black (#333333)
    - Icon color: primary system color (#336699)
  - **Toggled Mode** (after toggle button is pressed):
    - Background color: dark blue (#224466)
    - Text color: white (#FFFFFF)
    - Icon color: white (#FFFFFF)
  - Width: 250px (expanded), 60px (compact)
  - Height: 100% screen height
  - Fixed position (fixed-left)
  - Z-index: 1020
  - Switching between modes with toggle button in header
  - Toggle button uses sun (☀️) and moon (🌙) icons for color mode switching
  - Transition animation: smooth transition (transition: 0.3s ease-in-out)

- **Application Navigation**:
  - **Application Dropdown List**:
    - Each application displayed with icon and name
    - Hover effect: light blue (#4488BB) in dark mode, lighter gray (#EEEEEE) in light mode
    - Active application highlight: yellow line on left edge (#FFCC00)

  - **Application Model Selection**:
    - Each application has an opening section with its models
    - Model list as a submenu
    - Ability to configure which models are available to a specific user (depending on permissions)
    - Administration section allows defining model availability for user groups

- **Configuration Functionality**:
  - `settings.py` file contains application and model configuration for navigation:
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
        # other applications
    }
    ```

  - Middleware class checks user permissions and filters navigation elements

- **Dynamic Navigation Element Generation**:
  - Template tags functionality for navigation generation:
    ```python
    @register.inclusion_tag('core/navigation.html', takes_context=True)
    def render_navigation(context):
        user = context['request'].user
        apps = filter_navigation_by_permissions(NAVIGATION_APPS, user)
        return {'apps': apps}
    ```

- **Navigation Element Template Structure**:
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

### 1.4.4. User Interface Functionality
The user interface has the following functional requirements:

- **Responsive Design**:
  - Main content adapts to different screen resolutions
  - Side panels and headers shrink or hide on smaller screens
  - Navigation adapts to mobile devices (hamburger menu)

- **Interactive Components**:
  - Buttons, links, and menus respond to mouse clicks and touch gestures
  - Dynamic message and alert systems
  - Tooltips and instructions for new users

- **Customizable Settings**:
  - Users can customize interface settings (themes, languages, notifications)
  - Ability to save multiple themes and quickly switch between them
  - User preferences are saved in the database and loaded when logging in

- **Data Visualization**:
  - Charts, diagrams, and other visual elements for data display
  - Ability to export data to PDF, Excel, and other formats
  - Interactive diagrams with the ability to zoom, move, and click on elements

- **Accessibility**:
  - Compliance with WCAG 2.1 standards
  - Text alternatives for images and graphic elements
  - Keyboard navigation for all functions
  - Customizable text size and color contrast settings

## 1.5. Custom Management Commands (Automation Scripts)

Django provides the ability to create custom management commands that can be executed through `manage.py`. These commands are an effective way to automate repetitive tasks, data import/export, system maintenance, and other frequent processes.

### 1.5.1. Command Structure and Placement

Each application should follow this structure for custom command placement:

```
apps/APP_NAME/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       ├── command_name.py
│       └── another_command.py
```

### 1.5.2. Command File Structure

Each command is defined in a separate Python file with a class `Command` that inherits from `BaseCommand`:

```python
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.APP_NAME.models import Model

class Command(BaseCommand):
    help = 'Command description that will be shown when using help'

    def add_arguments(self, parser):
        # Required arguments
        parser.add_argument('position_arg', type=str, help='Positional argument description')
        
        # Optional arguments
        parser.add_argument(
            '--optional',
            '-o',
            dest='optional_arg',
            default='default_value',
            help='Optional argument description',
        )
        
        # Boolean flags
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output',
        )

    def handle(self, *args, **options):
        # Getting values from options
        verbose = options['verbose']
        position_arg = options['position_arg']
        
        try:
            # Command main logic
            if verbose:
                self.stdout.write(self.style.SUCCESS(f'Starting processing: {position_arg}'))
            
            # Database operations should be done within a transaction
            with transaction.atomic():
                # Command main operations
                records = Model.objects.filter(field=position_arg)
                
                for record in records:
                    # Perform operations with each record
                    self.process_record(record)
                    
                    # Progress information
                    if verbose:
                        self.stdout.write(f'Processed: {record}')
            
            # Successful result
            self.stdout.write(self.style.SUCCESS('Command successfully executed!'))
            
        except Exception as e:
            # Error handling
            raise CommandError(f'Error executing command: {str(e)}')
    
    def process_record(self, record):
        """Separate method for specific logic processing."""
        # Logic for record processing
        pass
```

### 1.5.3. Command Execution

Commands can be called through `manage.py`:

```bash
python manage.py command_name positional_arg --optional=custom_value --verbose
```

### 1.5.4. Best Practices

1. **Progress and Status Messages**:
   ```python
   # Success message
   self.stdout.write(self.style.SUCCESS('Success!'))
   
   # Warning
   self.stdout.write(self.style.WARNING('Warning!'))
   
   # Error
   self.stdout.write(self.style.ERROR('Error!'))
   
   # Regular text
   self.stdout.write('Information')
   ```

2. **Grouping Operations in Transactions**:
   ```python
   with transaction.atomic():
       # Operations that should happen atomically
   ```

3. **Permissible Error Handling**:
   ```python
   try:
       # Risky operations
   except SomeError as e:
       self.stdout.write(self.style.ERROR(f'Error: {e}'))
       # Return a meaningful error code that can be processed in automated processes
       return 1
   ```

4. **Interactive Requests**:
   ```python
   if options['interactive']:
       answer = input('Continue? [y/N]: ')
       if answer.lower() != 'y':
           self.stdout.write(self.style.WARNING('Operation cancelled.'))
           return
   ```

### 1.5.5. Practical Examples

#### 1. Data Export Command

```python
# apps/documents/management/commands/export_documents.py
from django.core.management.base import BaseCommand
import csv
import os
from apps.documents.models import Document

class Command(BaseCommand):
    help = 'Export documents in CSV format'

    def add_arguments(self, parser):
        parser.add_argument('--output', default='documents.csv', help='Output file path')
        parser.add_argument('--since', help='Documents created since (YYYY-MM-DD)')

    def handle(self, *args, **options):
        output_file = options['output']
        since_date = options['since']
        
        # Filter documents
        queryset = Document.objects.all()
        if since_date:
            queryset = queryset.filter(created_at__gte=since_date)
        
        count = queryset.count()
        self.stdout.write(f'Exporting {count} documents to {output_file}')
        
        # Export data
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['ID', 'Title', 'Creation Date', 'Status'])
            
            # Write data
            for doc in queryset:
                writer.writerow([
                    doc.id,
                    doc.title,
                    doc.created_at.strftime('%Y-%m-%d'),
                    doc.status
                ])
        
        self.stdout.write(self.style.SUCCESS(f'Successfully exported {count} documents.'))
```

#### 2. Data Import Command

```python
# apps/equipment/management/commands/import_equipment.py
from django.core.management.base import BaseCommand, CommandError
import csv
from apps.equipment.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Import equipment from CSV file'

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
                    # Find or create category
                    category, _ = EquipmentCategory.objects.get_or_create(
                        name=row['category']
                    )
                    
                    # Look for existing record
                    equipment = Equipment.objects.filter(
                        serial_number=row['serial_number']
                    ).first()
                    
                    if equipment:
                        if update:
                            # Update existing record
                            equipment.name = row['name']
                            equipment.category = category
                            equipment.purchase_date = row['purchase_date']
                            equipment.save()
                            updated += 1
                        else:
                            skipped += 1
                    else:
                        # Create new record
                        Equipment.objects.create(
                            name=row['name'],
                            serial_number=row['serial_number'],
                            category=category,
                            purchase_date=row['purchase_date']
                        )
                        created += 1
                
                self.stdout.write(self.style.SUCCESS(
                    f'Import completed: {created} created, {updated} updated, {skipped} skipped.'
                ))
                
        except FileNotFoundError:
            raise CommandError(f'File {file_path} not found')
        except Exception as e:
            raise CommandError(f'Error importing data: {str(e)}')
```

#### 3. System Maintenance Command

```python
# apps/core/management/commands/system_maintenance.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from datetime import datetime

class Command(BaseCommand):
    help = 'Perform system maintenance tasks'

    def add_arguments(self, parser):
        parser.add_argument('--full', action='store_true', help='Perform full maintenance')

    def handle(self, *args, **options):
        full = options['full']
        
        self.stdout.write('Starting system maintenance...')
        start_time = datetime.now()
        
        # Clean sessions
        self.stdout.write('Cleaning expired sessions...')
        call_command('clearsessions')
        
        # Clean various temporary data
        self.stdout.write('Deleting temporary files...')
        self._clean_temp_files()
        
        if full:
            # In full maintenance, optimize DB
            self.stdout.write('Optimizing database...')
            self._optimize_database()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.stdout.write(self.style.SUCCESS(
            f'System maintenance completed ({duration:.2f} seconds)'
        ))
    
    def _clean_temp_files(self):
        # Logic for cleaning temporary files would go here
        pass
    
    def _optimize_database(self):
        # PostgreSQL example
        with connection.cursor() as cursor:
            cursor.execute('VACUUM ANALYZE')
```

## 1.6. Information Input View

Data entry forms in the system are designed with the following principles:

- **Standard Input Form** (fits on one screen):
  - **Container**:
    - White background color (#FFFFFF)
    - Shadow: 0 2px 5px rgba(0,0,0,0.1)
    - Rounded corners: 5px
    - Maximum width: 1200px
    - Inner padding: 25px
    - Outer margin: auto (centered on screen)
  
  - **Title**:
    - Font size: 22px
    - Font weight: 600
    - Color: dark blue-gray (#334455)
    - Bottom border: 1px solid #EEEEEE
    - Bottom margin: 20px
  
  - **Field Organization**:
    - Grid layout (CSS Grid or Bootstrap)
    - On mobile devices switches to single column
    - Field groups visually separated with sections
    - Required fields marked with red asterisk (*)
  
  - **Input Fields**:
    - Label position: above field
    - Field height: 40px
    - Field borders: 1px solid #DDDDDD
    - Focus state: 1px solid #4488BB
    - Error state: 1px solid #FF4444
    - Inner padding: 10px
    - Space between fields: 15px
  
  - **Buttons**:
    - Primary button (Save): blue (#4488BB)
    - Secondary button (Cancel): gray (#CCCCCC)
    - Text color: white (#FFFFFF)
    - Button height: 40px
    - Button width: according to content, min 120px
    - Rounded corners: 4px
    - Button placement: bottom right corner

- **Extended Input Form** (information doesn't fit on one screen):
  - **Tab System**:
    - Tabs at the top dividing information into logical categories
    - Active tab: blue (#336699) with white text
    - Inactive tab: light gray (#F5F5F5) with dark text
    - Space between tabs: 2px
  
  - **Accordion Panels**:
    - Alternative to tabs for longer lists
    - Expandable/collapsible content
    - Header: gray background (#F5F5F5)
    - Icon indicates current state (expanded/closed)
  
  - **Navigation**:
    - Navigation buttons (Back/Next) between sequential steps
    - Progress indicator for multi-step forms
    - "Return to list" button in top right corner
  
  - **Wide Table Solutions**:
    - Horizontal scrolling for tables with many columns
    - Fixed table header when scrolling vertically
    - Ability to minimize or hide less important columns
    - "View all" button to open in full-screen view

- **Specific Case Examples**:
  - **Equipment Registry**:
    - Divided into tabs: "Basic Information", "Technical Specification", "Maintenance", "Documents"
    - Search filters expanded at the top, collapsible as needed
    - Common options in toolbar: "Export", "Print", "Filter"
    - Quick actions for each record: "View", "Edit", "Delete"
  
  - **Document Management**:
    - Document metadata in first tab, content in second tab
    - Document version history in separate panel
    - Related documents list in accordion section
    - Document approval workflow in separate block

- **Responsive Behavior**:
  - In smaller screens fields rearrange into single column
  - Tables switch to card view on mobile devices
  - Tabs switch to dropdown menu in narrow screens
  - Buttons adapt to screen size, maintaining reachability

## 1.7. Term Translation with Rosetta
Provide translation capabilities for all project terms using django-rosetta:

### 1.7.1. Installation
```
pip install django-rosetta
```

### 1.7.2. Configuration
Add Rosetta configuration to `config/settings.py`:
```python
INSTALLED_APPS = [
    # ...existing code...
    'rosetta',
    # ...existing code...
]

LANGUAGES = [
    ('lv', 'Latvian'),
    ('en', 'English'),
    # Add additional languages as needed
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

### 1.7.3. URL Configuration
Add Rosetta URLs to `config/urls.py`:
```python
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
```

### 1.7.4. Localization Directory Preparation
Create necessary folders and initial translation files:
```bash
mkdir -p locale/{lv,en}/LC_MESSAGES
django-admin makemessages -l lv
django-admin makemessages -l en
```

### 1.7.5. Text Marking in Models
Mark all translatable texts with gettext functions:
```python
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    name = models.CharField(_('name'), max_length=100)
```

### 1.7.6. Text Marking in Templates
In templates use:
```html
{% load i18n %}
<h1>{% trans "Welcome" %}</h1>
```

### 1.7.7. Translation Compilation
Compile translations:
```bash
django-admin compilemessages
```

### 1.7.8. Translation Administration
Access translation administration through the `/rosetta/` URL.

## 1.8. Existing Application Structure

### Users Application (`apps/users/`)
```
apps/users/
├── admin.py                 # User model admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # UserCreationForm, UserChangeForm
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── user.py              # CustomUser model
│   ├── profile.py           # UserProfile model
│   └── permissions.py       # User permission models
├── templates/
│   └── users/
│       ├── login.html       # User login template
│       ├── register.html    # Registration template
│       └── profile.html     # Profile page
├── static/
│   └── users/
│       ├── css/
│       │   └── user.css     # User styles
│       └── js/
│           └── profile.js   # Profile functionality
├── urls.py                  # Users application routes
├── views.py                 # User management views
└── tests.py                 # User tests
```

### Documents Application (`apps/documents/`)
```
apps/documents/
├── admin.py                 # Document admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Document forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── document.py          # Document base class
│   ├── section.py           # DocumentSection model
│   └── attachment.py        # Attachment model
├── templates/
│   └── documents/
│       ├── list.html        # Document list
│       ├── detail.html      # Document details
│       └── form.html        # Document forms
├── static/
│   └── documents/
│       ├── css/
│       │   └── documents.css # Document styles
│       └── js/
│           └── editor.js     # Document editor
├── urls.py                  # Document routes
├── views.py                 # Document processing views
└── tests.py                 # Document tests
```

### Equipment Application (`apps/equipment/`)
```
apps/equipment/
├── admin.py                 # Equipment admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Equipment forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── equipment.py         # Equipment model
│   ├── category.py          # EquipmentCategory model
│   └── maintenance.py       # Maintenance model
├── templates/
│   └── equipment/
│       ├── list.html        # Equipment list
│       ├── detail.html      # Equipment details
│       └── maintenance.html # Maintenance page
├── static/
│   └── equipment/
│       ├── css/
│       │   └── equipment.css # Equipment styles
│       └── js/
│           └── maintenance.js # Maintenance logic
├── urls.py                  # Equipment routes
├── views.py                 # Equipment processing views
└── tests.py                 # Equipment tests
```

### Audits Application (`apps/audits/`)
```
apps/audits/
├── admin.py                 # Audit admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Audit forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── audit.py             # Audit base class
│   ├── finding.py           # AuditFinding model
│   └── checklist.py         # AuditChecklist model
├── templates/
│   └── audits/
│       ├── list.html        # Audit list
│       ├── detail.html      # Audit details
│       └── report.html      # Audit report
├── static/
│   └── audits/
│       ├── css/
│       │   └── audits.css   # Audit styles
│       └── js/
│           └── checklist.js # Audit checklist logic
├── urls.py                  # Audit routes
├── views.py                 # Audit processing views
└── tests.py                 # Audit tests
```

### Accounts Application (`apps/accounts/`)
```
apps/accounts/
├── admin.py                 # Account admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Account forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── account.py           # Account model
│   └── subscription.py      # Subscription model
├── templates/
│   └── accounts/
│       ├── dashboard.html   # Account panel
│       ├── billing.html     # Billing management
│       └── settings.html    # Account settings
├── static/
│   └── accounts/
│       ├── css/
│       │   └── accounts.css # Account styles
│       └── js/
│           └── billing.js   # Payment processing
├── urls.py                  # Account routes
├── views.py                 # Account processing views
└── tests.py                 # Account tests
```

### Authentication Application (`apps/authentication/`)
```
apps/authentication/
├── admin.py                 # Authentication admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Authentication forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── token.py             # Token model
│   └── otp.py               # OTP model
├── templates/
│   └── authentication/
│       ├── login.html       # Login template
│       ├── register.html    # Registration template
│       └── reset.html       # Password reset template
├── static/
│   └── authentication/
│       ├── css/
│       │   └── auth.css     # Authentication styles
│       └── js/
│           └── otp.js       # OTP functionality
├── urls.py                  # Authentication routes
├── views.py                 # Authentication views
└── tests.py                 # Authentication tests
```

### Company Application (`apps/company/`)
```
apps/company/
├── admin.py                 # Company admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Company forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── company.py           # Company model
│   ├── department.py        # Department model
│   └── location.py          # Location model
├── templates/
│   └── company/
│       ├── list.html        # Company list
│       ├── detail.html      # Company details
│       └── org_chart.html   # Organization structure
├── static/
│   └── company/
│       ├── css/
│       │   └── company.css  # Company styles
│       └── js/
│           └── org_chart.js # Org. structure visualization
├── urls.py                  # Company routes
├── views.py                 # Company processing views
└── tests.py                 # Company tests
```

### Dashboard Application (`apps/dashboard/`)
```
apps/dashboard/
├── admin.py                 # Dashboard admin registration
├── apps.py                  # AppConfig configuration
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── widget.py            # Widget model
│   └── preference.py        # UserPreference model
├── templates/
│   └── dashboard/
│       ├── index.html       # Main panel
│       ├── widgets.html     # Widget configuration
│       └── charts.html      # Data visualizations
├── static/
│   └── dashboard/
│       ├── css/
│       │   └── dashboard.css # Panel styles
│       └── js/
│           ├── widgets.js    # Widget logic
│           └── charts.js     # Chart visualization
├── urls.py                  # Dashboard routes
├── views.py                 # Dashboard views
└── tests.py                 # Dashboard tests
```

### Methods Application (`apps/methods/`)
```
apps/methods/
├── admin.py                 # Method admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Method forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── method.py            # Method model
│   ├── validation.py        # MethodValidation model
│   └── parameter.py         # MethodParameter model
├── templates/
│   └── methods/
│       ├── list.html        # Method list
│       ├── detail.html      # Method details
│       └── validation.html  # Validation page
├── static/
│   └── methods/
│       ├── css/
│       │   └── methods.css  # Method styles
│       └── js/
│           └── validation.js # Validation logic
├── urls.py                  # Method routes
├── views.py                 # Method processing views
└── tests.py                 # Method tests
```

### Personnel Application (`apps/personnel/`)
```
apps/personnel/
├── admin.py                 # Personnel admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Personnel forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── employee.py          # Employee model
│   ├── position.py          # Position model
│   └── qualification.py     # Qualification model
├── templates/
│   └── personnel/
│       ├── list.html        # Employee list
│       ├── detail.html      # Employee details
│       └── training.html    # Training page
├── static/
│   └── personnel/
│       ├── css/
│       │   └── personnel.css # Personnel styles
│       └── js/
│           └── qualifications.js # Qualification management
├── urls.py                  # Personnel routes
├── views.py                 # Personnel processing views
└── tests.py                 # Personnel tests
```

### Standards Application (`apps/standards/`)
```
apps/standards/
├── admin.py                 # Standards admin registration
├── apps.py                  # AppConfig configuration
├── forms.py                 # Standards forms
├── migrations/              # DB migration files
├── models/                  # Package with models
│   ├── __init__.py          # Exports all models
│   ├── standard.py          # Standard model
│   ├── requirement.py       # Requirement model
│   └── compliance.py        # Compliance model
├── templates/
│   └── standards/
│       ├── list.html        # Standards list
│       ├── detail.html      # Standard details
│       └── compliance.html  # Compliance overview
├── static/
│   └── standards/
│       ├── css/
│       │   └── standards.css # Standards styles
│       └── js/
│           └── compliance.js # Compliance checks
├── urls.py                  # Standards routes
├── views.py                 # Standards processing views
└── tests.py                 # Standards tests
```