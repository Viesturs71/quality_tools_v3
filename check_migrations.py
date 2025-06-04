import os


def list_migrations(app_name):
    migration_path = os.path.join(os.getcwd(), app_name, 'migrations')
    if not os.path.exists(migration_path):
        return f"No migrations directory found for {app_name}"

    migrations = [f for f in os.listdir(migration_path) if f.endswith('.py') and not f.startswith('__')]
    return f"Migrations for {app_name}:\n" + "\n".join(migrations)

if __name__ == "__main__":
    pass
