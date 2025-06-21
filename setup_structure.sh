mkdir -p apps/{users,documents,equipment}/{migrations,templates,static,models}
mkdir -p apps/users/templates/users
mkdir -p apps/users/static/users/{css,js,img}
mkdir -p apps/documents/templates/documents
mkdir -p apps/documents/static/documents/{css,js,img}
mkdir -p apps/equipment/templates/equipment
mkdir -p apps/equipment/static/equipment/{css,js,img}
mkdir -p config
mkdir -p templates/{admin/includes,home}
mkdir -p static/{css,js,img}
touch manage.py
touch requirements.txt
touch .gitignore
touch Dockerfile
touch docker-compose.yml
mkdir -p .github/workflows
touch .github/workflows/ci.yml
