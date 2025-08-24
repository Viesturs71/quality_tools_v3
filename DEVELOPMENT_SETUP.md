# Development Setup

## Quick Start

To fix the `DJANGO_SECRET_KEY not found` error and get the project running:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Environment File**
   ```bash
   cp .env.example .env
   ```

3. **Run with Development Settings**
   ```bash
   python manage.py runserver --settings=config.settings.dev
   ```

## Environment Configuration

This project uses different settings configurations:

### Development (Recommended)
The `dev.py` settings include hardcoded values suitable for development:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py runserver
```

### Production
The `base.py` and `prod.py` settings require environment variables:
- Copy `.env.example` to `.env`
- Update environment variables in `.env` file
- Set `DJANGO_SETTINGS_MODULE=config.settings.prod`

## Environment Variables

Key variables required in `.env` file for base/production settings:

- `DJANGO_SECRET_KEY`: Django secret key for security
- `DEBUG`: Enable/disable debug mode
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string

## Troubleshooting

### DJANGO_SECRET_KEY Error
If you see `UndefinedValueError: DJANGO_SECRET_KEY not found`:

1. Make sure `.env` file exists with `DJANGO_SECRET_KEY` variable
2. Or use dev settings: `--settings=config.settings.dev`

### Import Errors
If you see module import errors, the project dependencies may not be installed:
```bash
pip install -r requirements.txt
```