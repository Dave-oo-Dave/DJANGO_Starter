import os
import subprocess
import re

def validate_name(name):
    """Ensure valid Python package name"""
    if not name or not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
        raise ValueError("Name must start with a letter and contain only letters, numbers, or underscores")

def create_traditional_project(project_path, project_name):
    """Create traditional Django structure matching the screenshot"""
    try:
        # Create virtual environment
        venv_path = os.path.join(project_path, 'venv')
        subprocess.run(f"python -m venv {venv_path}", shell=True, check=True)
        
        # Install Django
        install_cmd = f"""
        source {os.path.join(venv_path, 'bin/activate')} && \
        pip install django && \
        deactivate
        """
        subprocess.run(install_cmd, shell=True, executable='/bin/bash', check=True)
        
        # Create project structure (exactly as in screenshot)
        subprocess.run(
            f"cd {project_path} && \
            source {os.path.join(venv_path, 'bin/activate')} && \
            django-admin startproject {project_name} . && \
            deactivate",
            shell=True, executable='/bin/bash', check=True
        )
        
        # Run migrations to create db.sqlite3
        migrate_cmd = f"""
        cd {project_path} && \
        source {os.path.join(venv_path, 'bin/activate')} && \
        python manage.py migrate && \
        deactivate
        """
        subprocess.run(migrate_cmd, shell=True, executable='/bin/bash', check=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during setup: {e}")
        return False

def main():
    print("\n" + "="*50)
    print("Django Traditional Project Creator".center(50))
    print("="*50)
    
    # Get project name
    while True:
        project_name = input("\nEnter project name (e.g., my_project): ").strip()
        try:
            validate_name(project_name)
            break
        except ValueError as e:
            print(f"❌ {e}")
    
    # Create project folder on Desktop
    project_path = os.path.join(os.path.expanduser("~/Desktop"), project_name)
    try:
        os.makedirs(project_path, exist_ok=False)
    except FileExistsError:
        print(f"❌ Folder already exists: {project_path}")
        return
    
    # Create project
    if create_traditional_project(project_path, project_name):
        print(f"\n✅ Traditional structure created at:")
        print(f"{project_path}/")
        print(f"├── db.sqlite3")
        print(f"├── manage.py")
        print(f"├── {project_name}/")
        print(f"│   ├── __init__.py")
        print(f"│   ├── settings.py")
        print(f"│   ├── urls.py")
        print(f"│   ├── asgi.py")
        print(f"│   └── wsgi.py")
        print(f"└── venv/")
        
        print("\n🚀 Next steps:")
        print(f"cd {project_path}")
        print("source venv/bin/activate")
        print("python manage.py startapp my_app")
        print("python manage.py runserver")
    else:
        print("❌ Project creation failed")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()