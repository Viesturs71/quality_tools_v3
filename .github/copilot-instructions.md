GitHub Copilot Chat Instructions — Multi-App Django Project Structure: Management System Tools
1. Objective
Generate and maintain a clearly structured Django project directory and file layout for a large, multi-app system "Management System Tools": - Each application has its own folder under apps/ - Project-level template folder templates/ (admin-override + common layouts) - App-level template folder apps/APP_NAME/templates/APP_NAME/ - Model reorganization: apps/APP_NAME/models/ package, one file per class - Static resource separation: static/css, static/js, static/img - Git, Docker and CI basic configuration
1.1. Centralized Settings Management
The project uses centralized Django settings configuration, divided into multiple files:
•	config/settings/base.py – basic settings (common to all environments)
•	config/settings/dev.py – development environment settings (imports from base)
•	config/settings/prod.py – production environment settings (imports from base)
How to use:
The variable DJANGO_SETTINGS_MODULE points to the appropriate file: - In development environment: DJANGO_SETTINGS_MODULE=config.settings.dev - In production: DJANGO_SETTINGS_MODULE=config.settings.prod
1.2. Static Files and Template Reuse
Reusable template parts ("partials") should be placed in separate files:
templates/shared/header.html
templates/shared/footer.html
templates/shared/alerts.html
These partials should be included in the main templates: - With tag: {% include "shared/header.html" %} - Or by defining block sections that app templates can override
1.3. System Sections
Management System Tools consists of two main sections:
1.	Administration Section:
2.	Designed for administrators and system managers
3.	Provides ability to structure and organize system basic settings
4.	Allows entering necessary initial data before system usage
5.	Manages user permissions, access levels, and company structure
6.	Includes configuration settings and system parameters
7.	User Section:
8.	Designed for everyday users with various access levels
9.	Allows users to enter or view information according to assigned permissions
10.	Provides various functions depending on user role (reading, editing, approving)
11.	Includes document management, audits, methods, and other functional sections
12.	Provides workflows and information visualization
1.4. Unified Design
1.4.1. Administration Section Header
The administration section has a unified design with the following elements:
•	Left Side:
•	System name "Management System Tools"
•	Background color: primary system color (#336699)
•	Text color: white (#FFCC00)
•	Right Side (from right to left):
•	User Information:
o	Logged-in user's first and last name
o	Text color: yellow (#FFCC00)
o	Background: primary system color (#336699)
•	Navigation Buttons:
o	Switch to user section (icon + text "User Section")
o	Change password (icon + text "Change Password")
o	Log out (icon + text "Log Out")
o	Button color: light blue (#4488BB)
o	Text color: white (#FFFFFF)
•	Language Menu:
o	Dropdown menu with available languages (LV/EN)
o	Active language is highlighted in bold
•	Toggle Menu:
o	Three-line icon that opens/closes the side navigation panel
o	Color: white (#FFFFFF)
•	Fixed Position:
•	Header fixed at the top of the screen (fixed-top)
•	Height: 60px
•	Z-index: 1030
1.4.2. User Section Header
The user section has a unified design with the following elements:
•	Left Side:
•	Quick access to main sections (Dashboard, Profile, Settings)
•	Background color: light gray (#F7F7F7)
•	Text color: black (#333333)
•	Right Side (from right to left):
•	User Information:
o	Logged-in user's name
o	Text color: black (#333333)
o	Background: white (#FFFFFF)
o	Border: gray (#DDDDDD)
o	Rounded corners: 5px
o	Height: 40px
o	Inner padding: 10px 15px
•	Logout Button:
o	Icon (log out) + text "Log Out"
o	Button color: red (#FF4444)
o	Text color: white (#FFFFFF)
o	Rounded corners: 5px
o	Height: 40px
o	Inner padding: 10px 15px
o	Floating position in right corner
•	Fixed Position:
•	Header fixed at the top of the screen (fixed-top)
•	Height: 60px
•	Z-index: 1030
1.4.3. Navigation Panel
The system has a vertical navigation panel on the left side with the following elements:
•	Basic Structure:
•	Default Mode:
o	Background color: white (#FFFFFF)
o	Text color: black (#333333)
o	Icon color: primary system color (#336699)
•	Toggled Mode (after toggle button is pressed):
o	Background color: dark blue (#224466)
o	Text color: white (#FFFFFF)
o	Icon color: white (#FFFFFF)
•	Width: 250px (expanded), 60px (compact)
•	Height: 100% screen height
•	Fixed position (fixed-left)
•	Z-index: 1020
•	Switching between modes with toggle button in header
•	Toggle button uses sun (☀️) and moon (🌙) icons for color mode switching
•	Transition animation: smooth transition (transition: 0.3s ease-in-out)
•	Application Navigation:
•	Application Dropdown List:
o	Each application displayed with icon and name
o	Hover effect: light blue (#4488BB) in dark mode, lighter gray (#EEEEEE) in light mode
o	Active application highlight: yellow line on left edge (#FFCC00)
•	Application Model Selection:
o	Each application has an opening section with its models
o	Model list as a submenu
o	Ability to configure which models are available to a specific user (depending on permissions)
o	Administration section allows defining model availability for user groups
•	Configuration Functionality:
•	settings.py file contains application and model configuration for navigation:
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
•	Middleware class checks user permissions and filters navigation elements
•	Dynamic Navigation Element Generation:
•	Template tags functionality for navigation generation:
 	@register.inclusion_tag('core/navigation.html', takes_context=True)
def render_navigation(context):
    user = context['request'].user
    apps = filter_navigation_by_permissions(NAVIGATION_APPS, user)
    return {'apps': apps}
•	Navigation Element Template Structure:
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
1.4.4. User Interface Functionality
The user interface has the following functional requirements:
•	Responsive Design:
•	Main content adapts to different screen resolutions
•	Side panels and headers shrink or hide on smaller screens
•	Navigation adapts to mobile devices (hamburger menu)
•	Interactive Components:
•	Buttons, links, and menus respond to mouse clicks and touch gestures
•	Dynamic message and alert systems
•	Tooltips and instructions for new users
•	Customizable Settings:
•	Users can customize interface settings (themes, languages, notifications)
•	Ability to save multiple themes and quickly switch between them
•	User preferences are saved in the database and loaded when logging in
•	Data Visualization:
•	Charts, diagrams, and other visual elements for data display
•	Ability to export data to PDF, Excel, and other formats
•	Interactive diagrams with the ability to zoom, move, and click on elements
•	Accessibility:
•	Compliance with WCAG 2.1 standards
•	Text alternatives for images and graphic elements
•	Keyboard navigation for all functions
•	Customizable text size and color contrast settings
1.5. Custom Management Commands (Automation Scripts)
Django provides the ability to create custom management commands that can be executed through manage.py. These commands are an effective way to automate repetitive tasks, data import/export, system maintenance, and other frequent processes.
1.5.1. Command Structure and Placement
Each application should follow this structure for custom command placement:
apps/APP_NAME/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       ├── command_name.py
│       └── another_command.py
1.5.2. Command File Structure
Each command is defined in a separate Python file with a class Command that inherits from BaseCommand:
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
1.5.3. Command Execution
Commands can be called through manage.py:
python manage.py command_name positional_arg --optional=custom_value --verbose
1.5.4. Best Practices
1.	Progress and Status Messages:
 	# Success message
self.stdout.write(self.style.SUCCESS('Success!'))

# Warning
self.stdout.write(self.style.WARNING('Warning!'))

# Error
self.stdout.write(self.style.ERROR('Error!'))

# Regular text
self.stdout.write('Information')
2.	Grouping Operations in Transactions:
 	with transaction.atomic():
    # Operations that should happen atomically
3.	Permissible Error Handling:
 	try:
    # Risky operations
except SomeError as e:
    self.stdout.write(self.style.ERROR(f'Error: {e}'))
    # Return a meaningful error code that can be processed in automated processes
    return 1
4.	Interactive Requests:
 	if options['interactive']:
    answer = input('Continue? [y/N]: ')
    if answer.lower() != 'y':
        self.stdout.write(self.style.WARNING('Operation cancelled.'))
        return
1.5.5. Practical Examples
1. Data Export Command
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
2. Data Import Command
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
3. System Maintenance Command
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
1.6. Information Input View
Data entry forms in the system are designed with the following principles:
•	Standard Input Form (fits on one screen):
•	Container:
o	White background color (#FFFFFF)
o	Shadow: 0 2px 5px rgba(0,0,0,0.1)
o	Rounded corners: 5px
o	Maximum width: 1200px
o	Inner padding: 25px
o	Outer margin: auto (centered on screen)
•	Title:
o	Font size: 22px
o	Font weight: 600
o	Color: dark blue-gray (#334455)
o	Bottom border: 1px solid #EEEEEE
o	Bottom margin: 20px
•	Field Organization:
o	Grid layout (CSS Grid or Bootstrap)
o	On mobile devices switches to single column
o	Field groups visually separated with sections
o	Required fields marked with red asterisk (*)
•	Input Fields:
o	Label position: above field
o	Field height: 40px
o	Field borders: 1px solid #DDDDDD
o	Focus state: 1px solid #4488BB
o	Error state: 1px solid #FF4444
o	Inner padding: 10px
o	Space between fields: 15px
•	Buttons:
o	Primary button (Save): blue (#4488BB)
o	Secondary button (Cancel): gray (#CCCCCC)
o	Text color: white (#FFFFFF)
o	Button height: 40px
o	Button width: according to content, min 120px
o	Rounded corners: 4px
o	Button placement: bottom right corner
•	Extended Input Form (information doesn't fit on one screen):
•	Tab System:
o	Tabs at the top dividing information into logical categories
o	Active tab: blue (#336699) with white text
o	Inactive tab: light gray (#F5F5F5) with dark text
o	Space between tabs: 2px
•	Accordion Panels:
o	Alternative to tabs for longer lists
o	Expandable/collapsible content
o	Header: gray background (#F5F5F5)
o	Icon indicates current state (expanded/closed)
•	Navigation:
o	Navigation buttons (Back/Next) between sequential steps
o	Progress indicator for multi-step forms
o	"Return to list" button in top right corner
•	Wide Table Solutions:
o	Horizontal scrolling for tables with many columns
o	Fixed table header when scrolling vertically
o	Ability to minimize or hide less important columns
o	"View all" button to open in full-screen view
•	Specific Case Examples:
•	Equipment Registry:
o	Divided into tabs: "Basic Information", "Technical Specification", "Maintenance", "Documents"
o	Search filters expanded at the top, collapsible as needed
o	Common options in toolbar: "Export", "Print", "Filter"
o	Quick actions for each record: "View", "Edit", "Delete"
•	Document Management:
o	Document metadata in first tab, content in second tab
o	Document version history in separate panel
o	Related documents list in accordion section
o	Document approval workflow in separate block
•	Responsive Behavior:
•	In smaller screens fields rearrange into single column
•	Tables switch to card view on mobile devices
•	Tabs switch to dropdown menu in narrow screens
•	Buttons adapt to screen size, maintaining reachability
1.7. Term Translation with Rosetta
Provide translation capabilities for all project terms using django-rosetta:
1.7.1. Installation
pip install django-rosetta
1.7.2. Configuration
Add Rosetta configuration to config/settings.py:
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
1.7.3. URL Configuration
Add Rosetta URLs to config/urls.py:
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
1.7.4. Localization Directory Preparation
Create necessary folders and initial translation files:
mkdir -p locale/{lv,en}/LC_MESSAGES
django-admin makemessages -l lv
django-admin makemessages -l en
1.7.5. Text Marking in Models
Mark all translatable texts with gettext functions:
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    name = models.CharField(_('name'), max_length=100)
1.7.6. Text Marking in Templates
In templates use:
{% load i18n %}
<h1>{% trans "Welcome" %}</h1>
1.7.7. Translation Compilation
Compile translations:
django-admin compilemessages
1.7.8. Translation Administration
Access translation administration through the /rosetta/ URL.
1.7.9. Language Choice and Code Terminology
The system must offer users a way to select their preferred interface language (for example, Latvian or English). Add a language selector (e.g. LV/EN) to the navigation bar or user settings so users can switch languages at runtime. While the user interface should be translated according to the chosen language, all internal code identifiers—such as model and field names, constants, and variables—must remain in English. Only user‑facing strings should be marked for translation and localized via Django’s i18n framework. This ensures that code remains readable and consistent while the application delivers a localized experience to end users.
1.8. Existing Application Structure
Users Application (apps/users/)
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
Documents Application (apps/documents/)
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
Equipment Application (apps/equipment/)
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
Audits Application (apps/audits/)
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
Accounts Application (apps/accounts/)
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
Authentication Application (apps/authentication/)
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
Company Application (apps/company/)
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
Dashboard Application (apps/dashboard/)
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
Methods Application (apps/methods/)
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
Personnel Application (apps/personnel/)
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
Standards Application (apps/standards/)
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
1.9. Standard-Document Linking
The system requires functionality to link standard sections (points, subpoints) with documents that demonstrate compliance with those standards. This creates a bidirectional traceability between standards and implementation documents.
1.9.1. Data Model Relationships
Standards and documents should be linked through a many-to-many relationship model:
# apps/standards/models/standard_compliance.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class StandardDocumentLink(models.Model):
    """
    Represents a link between a standard section and a document that demonstrates compliance.
    """
    standard_section = models.ForeignKey(
        'standards.StandardSection',
        on_delete=models.CASCADE,
        related_name='document_links',
        verbose_name=_('Standard Section')
    )
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name='standard_links',
        verbose_name=_('Document')
    )
    compliance_status = models.CharField(
        _('Compliance Status'),
        max_length=20,
        choices=[
            ('compliant', _('Compliant')),
            ('partial', _('Partially Compliant')),
            ('non_compliant', _('Non-Compliant')),
            ('not_applicable', _('Not Applicable')),
            ('in_progress', _('Implementation in Progress')),
        ],
        default='compliant'
    )
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_standard_links',
        verbose_name=_('Created By')
    )

    class Meta:
        verbose_name = _('Standard-Document Link')
        verbose_name_plural = _('Standard-Document Links')
        unique_together = ('standard_section', 'document')
        ordering = ('standard_section__code', 'document__title')

    def __str__(self):
        return f"{self.standard_section.code} → {self.document.title}"
1.9.2. Interface Implementation
Standard Detail View
When viewing a standard or standard section, the interface should:
1.	Display a list of linked documents with compliance status
2.	Provide a way to add new document links
3.	Allow filtering documents by compliance status
4.	Show compliance statistics (percentage of compliant documents)
Example implementation:
<!-- templates/standards/standard_detail.html -->
<div class="standard-section">
    <h3>{{ standard_section.code }} - {{ standard_section.title }}</h3>
    <div class="description">{{ standard_section.description }}</div>

    <div class="compliance-stats">
        <div class="progress">
            <div class="progress-bar" role="progressbar" 
                 style="width: {{ compliance_percentage }}%;" 
                 aria-valuenow="{{ compliance_percentage }}" 
                 aria-valuemin="0" aria-valuemax="100">
                {{ compliance_percentage }}% Compliant
            </div>
        </div>
    </div>

    <div class="linked-documents">
        <h4>{% trans "Linked Documents" %}</h4>
        <div class="filter-controls">
            <select class="form-select" id="compliance-filter">
                <option value="all">{% trans "All" %}</option>
                <option value="compliant">{% trans "Compliant" %}</option>
                <option value="partial">{% trans "Partially Compliant" %}</option>
                <option value="non_compliant">{% trans "Non-Compliant" %}</option>
                <option value="in_progress">{% trans "In Progress" %}</option>
            </select>
            <button class="btn btn-primary" id="add-document-link">
                {% trans "Add Document Link" %}
            </button>
        </div>

        <table class="table table-striped">
            <thead>
                <tr>
                    <th>{% trans "Document" %}</th>
                    <th>{% trans "Status" %}</th>
                    <th>{% trans "Notes" %}</th>
                    <th>{% trans "Actions" %}</th>
                </tr>
            </thead>
            <tbody>
                {% for link in document_links %}
                <tr data-status="{{ link.compliance_status }}">
                    <td>
                        <a href="{% url 'documents:detail' link.document.id %}">
                            {{ link.document.title }}
                        </a>
                    </td>
                    <td>
                        <span class="badge bg-{{ link.get_status_color }}">
                            {{ link.get_compliance_status_display }}
                        </span>
                    </td>
                    <td>{{ link.notes }}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary edit-link" 
                                data-link-id="{{ link.id }}">
                            {% trans "Edit" %}
                        </button>
                        <button class="btn btn-sm btn-outline-danger delete-link" 
                                data-link-id="{{ link.id }}">
                            {% trans "Remove" %}
                        </button>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="4">{% trans "No documents linked to this standard section." %}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
Document Detail View
When viewing a document, the interface should:
1.	Display a list of standard sections that this document addresses
2.	Provide a way to link the document to additional standard sections
3.	Allow categorization of links by compliance status
Example implementation:
<!-- templates/documents/document_detail.html -->
<div class="linked-standards">
    <h4>{% trans "Standard Compliance" %}</h4>
    <div class="actions">
        <button class="btn btn-primary" id="link-to-standard">
            {% trans "Link to Standard" %}
        </button>
    </div>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>{% trans "Standard Section" %}</th>
                <th>{% trans "Status" %}</th>
                <th>{% trans "Notes" %}</th>
                <th>{% trans "Actions" %}</th>
            </tr>
        </thead>
        <tbody>
            {% for link in standard_links %}
            <tr>
                <td>
                    <a href="{% url 'standards:section_detail' link.standard_section.id %}">
                        {{ link.standard_section.code }} - {{ link.standard_section.title }}
                    </a>
                </td>
                <td>
                    <span class="badge bg-{{ link.get_status_color }}">
                        {{ link.get_compliance_status_display }}
                    </span>
                </td>
                <td>{{ link.notes }}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary edit-link" 
                            data-link-id="{{ link.id }}">
                        {% trans "Edit" %}
                    </button>
                    <button class="btn btn-sm btn-outline-danger delete-link" 
                            data-link-id="{{ link.id }}">
                        {% trans "Remove" %}
                    </button>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4">{% trans "This document is not linked to any standard sections." %}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
1.9.3. Link Creation Modal
A modal dialog for creating/editing links between standards and documents:
<!-- templates/shared/standard_document_link_modal.html -->
<div class="modal fade" id="standardDocumentLinkModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{% trans "Link Standard to Document" %}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="standardDocumentLinkForm">
                    {% csrf_token %}
                    <input type="hidden" name="link_id" id="link_id">

                    <div class="mb-3">
                        <label for="standard_section" class="form-label">{% trans "Standard Section" %}</label>
                        <select class="form-select" id="standard_section" name="standard_section" required>
                            <option value="">{% trans "Select a standard section" %}</option>
                            {% for section in available_sections %}
                            <option value="{{ section.id }}">{{ section.code }} - {{ section.title }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="document" class="form-label">{% trans "Document" %}</label>
                        <select class="form-select" id="document" name="document" required>
                            <option value="">{% trans "Select a document" %}</option>
                            {% for doc in available_documents %}
                            <option value="{{ doc.id }}">{{ doc.title }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="compliance_status" class="form-label">{% trans "Compliance Status" %}</label>
                        <select class="form-select" id="compliance_status" name="compliance_status" required>
                            <option value="compliant">{% trans "Compliant" %}</option>
                            <option value="partial">{% trans "Partially Compliant" %}</option>
                            <option value="non_compliant">{% trans "Non-Compliant" %}</option>
                            <option value="not_applicable">{% trans "Not Applicable" %}</option>
                            <option value="in_progress">{% trans "Implementation in Progress" %}</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="notes" class="form-label">{% trans "Notes" %}</label>
                        <textarea class="form-control" id="notes" name="notes" rows="3"></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{% trans "Cancel" %}</button>
                <button type="button" class="btn btn-primary" id="saveLink">{% trans "Save" %}</button>
            </div>
        </div>
    </div>
</div>
1.9.4. API for Standard-Document Linking
Create API endpoints to manage the links:
# apps/standards/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import StandardDocumentLink
from .serializers import StandardDocumentLinkSerializer

class StandardDocumentLinkViewSet(viewsets.ModelViewSet):
    queryset = StandardDocumentLink.objects.all()
    serializer_class = StandardDocumentLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = StandardDocumentLink.objects.all()

        # Filter by standard section if provided
        standard_section_id = self.request.query_params.get('standard_section', None)
        if standard_section_id:
            queryset = queryset.filter(standard_section_id=standard_section_id)

        # Filter by document if provided
        document_id = self.request.query_params.get('document', None)
        if document_id:
            queryset = queryset.filter(document_id=document_id)

        # Filter by compliance status if provided
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(compliance_status=status)

        return queryset
1.9.5. Compliance Reporting
Create a report view that shows compliance across all standards:
# apps/standards/views.py
from django.views.generic import TemplateView
from django.db.models import Count, Case, When, IntegerField
from .models import StandardSection, StandardDocumentLink

class ComplianceReportView(TemplateView):
    template_name = "standards/compliance_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all top-level standards
        standards = StandardSection.objects.filter(parent=None)

        # For each standard, calculate compliance statistics
        standards_data = []
        for standard in standards:
            # Get all sections (including subsections) for this standard
            sections = StandardSection.objects.filter(
                models.Q(id=standard.id) | models.Q(parent=standard)
            )
            section_ids = [s.id for s in sections]

            # Count links by compliance status
            links_by_status = StandardDocumentLink.objects.filter(
                standard_section_id__in=section_ids
            ).aggregate(
                total=Count('id'),
                compliant=Count(Case(
                    When(compliance_status='compliant', then=1),
                    output_field=IntegerField()
                )),
                partial=Count(Case(
                    When(compliance_status='partial', then=1),
                    output_field=IntegerField()
                )),
                non_compliant=Count(Case(
                    When(compliance_status='non_compliant', then=1),
                    output_field=IntegerField()
                )),
                in_progress=Count(Case(
                    When(compliance_status='in_progress', then=1),
                    output_field=IntegerField()
                ))
            )

            # Calculate compliance percentage
            total = links_by_status['total']
            compliant = links_by_status['compliant']
            compliance_percentage = (compliant / total * 100) if total > 0 else 0

            standards_data.append({
                'standard': standard,
                'sections_count': len(sections),
                'links_by_status': links_by_status,
                'compliance_percentage': round(compliance_percentage, 1)
            })

        context['standards_data'] = standards_data
        return context
This provides comprehensive functionality for linking standards and documents, tracking compliance status, and generating compliance reports across the quality management system.
1.	Introduction The standards app provides management of quality‐management standards and their sections, links documents to standards, tracks compliance status, and records change history. Key features: Building a standards hierarchy (StandardCategory → Standard → StandardSection). Defining standard requirements and specifying their order. Linking documents to standards and tracking their compliance status. Recording change history and revisions.
2.	Model Overview and Relationships (Here you would list each model and how they relate—for example, that StandardCategory contains many Standard, each Standard contains many StandardSection, etc.)
StandardCategory └─ Standard └─ StandardSection (recursive) ├─ StandardRequirement ├─ StandardAttachment ├─ StandardDocument (independent) ├─ StandardCompliance ├─ StandardSectionDocumentLink └─ StandardRevision StandardCategory: highest level grouping (e.g., ISO, DIN). Standard: specific standard definition with code and name. StandardSection: standard sections (recursive, can have subsections). StandardRequirement: standard section requirement with unique code, description, and sequence. StandardAttachment: additional data units (e.g., PDF, links) for standard sections. StandardDocument: user-uploaded document to link with standards. StandardCompliance: implementation tracking (e.g., compliant, partial, in_progress). StandardSectionDocumentLink: connection model linking StandardSection and StandardDocument with implementation status and notes. StandardRevision: change history records for standard section or requirement content.
1.10. Security and Deployment Considerations
Maintaining a production‑ready Django system requires attention not only to structure and user experience but also to security practices and deployment environment constraints. The following guidelines summarise key recommendations from the OWASP Django Security Cheat Sheet and Heroku’s deployment documentation.
1.10.1. Secret Key and Sensitive Parameter Management
Never commit the project’s SECRET_KEY or other sensitive credentials to version control. OWASP recommends loading secrets from environment variables or secret‑manager services and generating sufficiently long random keys[1]. Use .env files locally or Heroku Config Vars in production to supply the SECRET_KEY, database passwords and API keys securely[1].
1.10.2. Security Middleware and HTTPS
Enable django.middleware.security.SecurityMiddleware in the MIDDLEWARE list to insert useful security headers[2]. In production set SECURE_CONTENT_TYPE_NOSNIFF = True and define SECURE_HSTS_SECONDS to enable HTTP Strict Transport Security, forcing browsers to use HTTPS[2]. Ensure that SECURE_SSL_REDIRECT = True, which automatically redirects all HTTP requests to HTTPS[3].
1.10.3. Secure Cookies and CSRF
Set SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE so cookies are transmitted only over HTTPS[4]. Always include {% csrf_token %} in HTML forms and ensure that CsrfViewMiddleware is enabled to protect against cross‑site request forgery[5].
1.10.4. XSS Protection
Rely on Django’s template engine auto‑escaping features and avoid using mark_safe or the |safe filter on untrusted content[6]. This prevents cross‑site scripting (XSS) vulnerabilities by treating all user input as untrusted.
1.10.5. Admin Panel URL Hardening
Rename the default /admin/ route to a non‑standard path (e.g., /system-admin/) to reduce exposure to automated attacks[7]. Combine this with strong authentication and limited access for admin users.
1.10.6. Cookie and Cache Policy
Configure X_FRAME_OPTIONS = 'DENY' or 'SAMEORIGIN' to mitigate clickjacking and define a Content‑Security‑Policy header when embedding third‑party scripts[2]. These headers instruct browsers on how to treat your content within iframes and scripts.
1.10.7. Allowed Hosts and CORS
Explicitly set the ALLOWED_HOSTS list in settings to restrict which domain names can serve the application. If the API is accessed from other domains, use the django-cors-headers package to define allowed origins and configure CORS appropriately.
1.10.8. Migrations and Custom User Model
Keep each app’s migration files in its migrations/ folder and include them in version control. Wherever a user reference is needed, call get_user_model() or use settings.AUTH_USER_MODEL rather than hard‑coding auth.User. This ensures compatibility with the custom CustomUser model.
1.10.9. Additional Definitions
•	Logging: Configure structured logging in settings with handlers that write to files or external services. Capture errors and warnings to aid monitoring and debugging.
•	Error Handling: Provide custom 404 and 500 templates so that users never see raw tracebacks or sensitive information.
•	Backups and Data Security: Document a strategy for regular database backups and secure storage. Use encryption for data at rest and in transit and define restore procedures.
1.10.10. Heroku Deployment and Data Storage
Heroku dynos have an ephemeral filesystem: any files created at runtime are lost when the dyno restarts[8]. Do not store user uploads or media files locally; instead configure an external storage service such as Amazon S3, Google Cloud Storage or a Heroku add‑on. Store the necessary access credentials (e.g., AWS keys) in Heroku Config Vars[9]. Static files should be served via a CDN or using Django’s collectstatic mechanism, and database backups should be stored securely off the dyno.
4. Model Field and Relationship Description
4.1. StandardCategory
•	code (CharField): category code, unique.
•	title (CharField): name.
•	description (TextField): description.
4.2. Standard
•	category (ForeignKey → StandardCategory): reference to category.
•	code (CharField): standard code.
•	title (CharField): name.
•	description (TextField): description.
4.3. StandardSection
•	standard (ForeignKey → Standard): reference to standard.
•	parent (ForeignKey self, null=True): for creating subsections.
•	code (CharField): section code.
•	title (CharField): name.
•	description (TextField): description.
4.4. StandardRequirement
•	section (ForeignKey → StandardSection): reference.
•	code (CharField): requirement code.
•	text (TextField): requirement description.
•	order (IntegerField): sequence number determining row order.
4.5. StandardAttachment
•	section (ForeignKey → StandardSection): reference.
•	file (FileField/URLField): attached file or link.
•	description (CharField): description.
4.6. StandardDocument
•	title (CharField): document name.
•	file (FileField): uploaded document.
•	uploaded_at (DateTimeField): upload time.
•	uploaded_by (ForeignKey → CustomUser): user.
4.7. StandardCompliance
•	requirement (ForeignKey → StandardRequirement): requirement.
•	user (ForeignKey → CustomUser): user tracking compliance.
•	status (CharField): implementation status (compliant, partial, non_compliant, in_progress).
•	notes (TextField): notes.
•	recorded_at (DateTimeField): time.
4.8. StandardSectionDocumentLink
•	standard_section (ForeignKey → StandardSection)
•	document (ForeignKey → StandardDocument)
•	compliance_status (CharField): same as StandardCompliance.status.
•	notes, created_at, updated_at.
•	created_by (ForeignKey → CustomUser).
4.9. StandardRevision
•	section or requirement (GenericForeignKey): where to perform revision.
•	changed_by (ForeignKey → CustomUser)
•	change_type (CharField): e.g., update, delete.
•	timestamp (DateTimeField)
•	diff (TextField): description of changes.
