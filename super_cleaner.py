import difflib
import os
import shutil

# Konfigurācija
PROJECT_ROOT = '.'
BACKUP_FOLDER = 'project_backup'
INVENTORY_REPORT = 'inventory_report.txt'
CURRENT_SCRIPT = os.path.basename(__file__)
PROTECTED_FILES = {CURRENT_SCRIPT, INVENTORY_REPORT}
SCAN_EXTENSIONS = {'.py', '.html', '.js'}
FOLDER_SIMILARITY_THRESHOLD = 0.8  # 80% līdzības slieksnis

# Helper funkcijas
def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

def backup_project():
    if os.path.exists(BACKUP_FOLDER):
        pass
    else:
        shutil.copytree(PROJECT_ROOT, BACKUP_FOLDER, dirs_exist_ok=True)

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

def delete_files(files):
    for file in files:
        if os.path.basename(file) in PROTECTED_FILES:
            continue
        try:
            os.remove(os.path.join(PROJECT_ROOT, file))
        except Exception:
            pass

def delete_empty_folders(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
            except Exception:
                pass

def load_project_sources():
    sources = []
    for root, _dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            if os.path.splitext(file)[1].lower() in SCAN_EXTENSIONS:
                try:
                    with open(os.path.join(root, file), encoding='utf-8') as f:
                        sources.append(f.read().lower())
                except Exception:
                    continue
    return sources

def find_unused_folders(project_sources):
    all_folders = set()
    for root, dirs, _files in os.walk(PROJECT_ROOT):
        for d in dirs:
            full_path = os.path.relpath(os.path.join(root, d), PROJECT_ROOT)
            all_folders.add(full_path.replace('\\', '/'))

    used_folders = set()
    for folder in all_folders:
        for source in project_sources:
            if f"/{folder}/" in source or f"{folder}/" in source or f"/{folder}" in source:
                used_folders.add(folder)
                break

    unused_folders = all_folders - used_folders
    return sorted(unused_folders)

def find_similar_folders(all_folders):
    similar_pairs = []
    folders_list = list(all_folders)
    for i in range(len(folders_list)):
        for j in range(i+1, len(folders_list)):
            ratio = difflib.SequenceMatcher(None, folders_list[i], folders_list[j]).ratio()
            if ratio >= FOLDER_SIMILARITY_THRESHOLD:
                similar_pairs.append((folders_list[i], folders_list[j], f"{ratio*100:.1f}%"))
    return similar_pairs

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

    delete_empty_folders(PROJECT_ROOT)

    sources = load_project_sources()
    unused_folders = find_unused_folders(sources)

    if unused_folders:
        for folder in unused_folders:
            try:
                shutil.rmtree(os.path.join(PROJECT_ROOT, folder))
            except Exception:
                pass
    else:
        pass

    similar_folders = find_similar_folders(set(unused_folders))

    with open('cleanup_summary.txt', 'w', encoding='utf-8') as report:
        report.write("Unused folders dzēsti:\n")
        for folder in unused_folders:
            report.write(f"- {folder}\n")
        report.write("\nAtrastie līdzīgie folderi:\n")
        for f1, f2, ratio in similar_folders:
            report.write(f"- {f1} <-> {f2} ({ratio})\n")

