import os
import shutil

# Konfigurācija
PROJECT_ROOT = '.'  # Strādāt no pašreizējās mapes
BACKUP_FOLDER = 'project_backup'
INVENTORY_REPORT = 'inventory_report.txt'
CURRENT_SCRIPT = os.path.basename(__file__)
PROTECTED_FILES = {CURRENT_SCRIPT, INVENTORY_REPORT}

# Helper funkcija, lai formatētu faila izmēru
def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

# Izveido projekta backup
def backup_project():
    if os.path.exists(BACKUP_FOLDER):
        pass
    else:
        shutil.copytree(PROJECT_ROOT, BACKUP_FOLDER, dirs_exist_ok=True)

# Iegūst failus, kurus vajadzētu dzēst
def get_files_to_delete():
    files_to_delete = []
    if not os.path.exists(INVENTORY_REPORT):
        return files_to_delete

    with open(INVENTORY_REPORT, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 5:
                path = parts[0].strip()
                action = parts[-1].strip()
                if action == 'ACTION: DELETE':
                    files_to_delete.append(path)
    return files_to_delete

# Dzēš failus
def delete_files(files):
    for file in files:
        if os.path.basename(file) in PROTECTED_FILES:
            continue
        try:
            os.remove(os.path.join(PROJECT_ROOT, file))
        except Exception:
            pass

if __name__ == '__main__':

    backup_project()
    files_to_delete = get_files_to_delete()

    if files_to_delete:
        for _file in files_to_delete:
            pass

        confirmation = input("\nVai tiešām dzēst šos failus? (jā/nē): ").lower()
        if confirmation in ('jā', 'yes', 'y'):
            delete_files(files_to_delete)
        else:
            pass
    else:
        pass
