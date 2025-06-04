import os

def create_app_structure():
    # List of apps needing models directory
    apps = ['accounts', 'companies', 'company', 'dashboard', 'equipment', 
            'methods', 'myproject', 'personnel', 'quality_docs', 'standards', 'users']
    
    # Create models directory with __init__.py for each app
    for app in apps:
        models_dir = os.path.join(app, 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        # Create __init__.py if it doesn't exist
        init_file = os.path.join(models_dir, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Import all models\n')
    
    # Create template directories for each app
    templates_dir = 'templates'
    os.makedirs(templates_dir, exist_ok=True)
    
    for app in apps:
        app_templates = os.path.join(templates_dir, app)
        os.makedirs(app_templates, exist_ok=True)
        
        # Add .gitkeep to ensure directory is tracked
        gitkeep = os.path.join(app_templates, '.gitkeep')
        if not os.path.exists(gitkeep):
            with open(gitkeep, 'w') as f:
                pass

if __name__ == "__main__":
    create_app_structure()
    print("Directory structure created successfully!")
