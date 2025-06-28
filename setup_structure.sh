#!/bin/bash

# Create the Django project structure with updated settings configuration
echo "Creating Django project structure..."

# Create config directory with settings package
mkdir -p config/settings
touch config/__init__.py
touch config/settings/__init__.py
touch config/settings/base.py
touch config/settings/dev.py
touch config/settings/prod.py
touch config/urls.py
touch config/wsgi.py
touch config/asgi.py

# Create apps directory with all required applications
mkdir -p apps/{users,documents,equipment,personnel,standards,dashboard,accounts,authentication,company,debug_tools}/{migrations,templates,static,models,management/commands}

# Initialize Python packages
find apps -type d -exec touch {}/__init__.py \;
find apps -type d -name "management" -exec touch {}/commands/__init__.py \;

# Create template directories for each app
for app in users documents equipment personnel standards dashboard accounts authentication company; do
    mkdir -p apps/$app/templates/$app
    mkdir -p apps/$app/static/$app/{css,js,img}
done

# Create project-level directories
mkdir -p templates/{admin/includes,shared,home}
mkdir -p static/{css,js,img}
mkdir -p locale/{en,lv}/LC_MESSAGES
mkdir -p media
mkdir -p logs

# Create main project files
touch manage.py
touch requirements.txt
touch .gitignore
touch README.md

# Create Docker files
touch Dockerfile
touch docker-compose.yml

# Create CI files
mkdir -p .github/workflows
touch .github/workflows/ci.yml

# Create environment scripts
echo "Creating environment setup scripts..."
cat > set_dev_env.sh << 'EOL'
#!/bin/bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
export DJANGO_ENVIRONMENT=dev
echo "Development environment variables set."
EOL

cat > set_prod_env.sh << 'EOL'
#!/bin/bash
export DJANGO_SETTINGS_MODULE=config.settings.prod
export DJANGO_ENVIRONMENT=prod
echo "Production environment variables set."
EOL

# Make scripts executable
chmod +x set_dev_env.sh
chmod +x set_prod_env.sh

# Create documentation files
touch copilot-instructions.md
mkdir -p .github/.qodo
cp copilot-instructions.md .github/.qodo/copilot-instructions-en.md

# Set proper permissions
chmod +x setup_structure.sh

echo "Django project structure created successfully."
echo "Use 'source set_dev_env.sh' to set up development environment."
echo "Use 'source set_prod_env.sh' to set up production environment."
