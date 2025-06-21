# Django Multi-App Project

A well-structured Django project following the multi-app architecture pattern.

## Project Structure

The project follows a consistent directory layout:

```
<project_root>/
├── apps/               # All feature apps (users, documentation, products, etc.)
├── config/             # Django settings, URLs, WSGI/ASGI, etc.
├── templates/          # Project-level templates
├── static/             # Project-level static files
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Docker Deployment

The project includes Docker configuration for easy deployment:

```bash
docker-compose up -d
```

## Project Guidelines

This project follows the structure guidelines defined in `.github/copilot-instructions.md`.
