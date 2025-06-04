import os

# Konfigurācija
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # vai '.' ja skripts ir projekta saknē
SIZE_THRESHOLD_MB = 5  # Faili lielāki par 5MB tiek uzskatīti par aizdomīgiem
EXTENSIONS_TO_FLAG = {'.json', '.sqlite3', '.log', '.tmp', '.txt'}
FOLDERS_TO_FLAG = {'staticfiles', 'locale'}
SCAN_EXTENSIONS = {'.py', '.html', '.js', '.css', '.txt'}

# Helper funkcija, lai formatētu faila izmēru
def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

# Ielādē visus failu saturus, kur meklēsim atsauces
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

# Galvenā funkcija, kas ģenerē dzēšanas sarakstu
def generate_cleanup_report():
    report = []
    project_sources = load_project_sources()

    for root, _dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, PROJECT_ROOT)
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file)[1].lower()

            # Analīzes kritēriji
            reasons = []

            if any(folder in root.split(os.sep) for folder in FOLDERS_TO_FLAG):
                reasons.append("Located in flagged folder")
            if file_ext in EXTENSIONS_TO_FLAG:
                reasons.append(f"Flagged extension {file_ext}")
            if file_size > SIZE_THRESHOLD_MB * 1024 * 1024:
                reasons.append(f"Large file ({format_size(file_size)})")

            if reasons:
                # Pārbauda vai fails tiek izmantots
                base_name = os.path.basename(file).lower()
                usage_found = any(base_name in source for source in project_sources)
                report.append({
                    'path': rel_path,
                    'size': format_size(file_size),
                    'reasons': ", ".join(reasons),
                    'used': usage_found
                })

    return report

# Izvada atskaiti uz ekrāna un saglabā failā
def save_report(report, filename='inventory_report.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in report:
            action = 'KEEP' if item['used'] else 'DELETE'
            line = f"{item['path']} | {item['size']} | {item['reasons']} | USED: {item['used']} | ACTION: {action}\n"
            f.write(line)

if __name__ == '__main__':
    cleanup_report = generate_cleanup_report()

    if cleanup_report:
        save_report(cleanup_report)
    else:
        pass
