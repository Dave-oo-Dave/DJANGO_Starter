import os
import subprocess
import re

def validate_name(name, name_type="project"):
    """Validate project or app names."""
    if not name:
        raise ValueError(f"{name_type.capitalize()} name cannot be empty")

    if name_type == "app":
        if not re.match(r'^[a-z][a-z0-9_]*$', name):
            raise ValueError("App names must be lowercase, start with a letter, and contain only letters, numbers, or underscores")
    else:
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
            raise ValueError("Project names should start with a letter and contain only letters, numbers, or underscores")

    python_keywords = {'email', 'admin', 'test', 'api', 'user'}  # Common conflicts
    if name.lower() in python_keywords:
        raise ValueError(f"'{name}' is a common conflict name")

def create_traditional_project(project_path, project_name):
    """Create a traditional Django project structure with virtual environment."""
    try:
        venv_path = os.path.join(project_path, 'venv')

        # Create virtual environment
        subprocess.run(f"python -m venv {venv_path}", shell=True, check=True)

        # Install Django inside the venv
        install_cmd = f"""
        source {os.path.join(venv_path, 'bin/activate')} && \
        pip install django && \
        deactivate
        """
        subprocess.run(install_cmd, shell=True, executable='/bin/bash', check=True)

        # Create Django project inside project_path
        create_cmd = f"""
        cd {project_path} && \
        source {os.path.join(venv_path, 'bin/activate')} && \
        django-admin startproject {project_name} . && \
        deactivate
        """
        subprocess.run(create_cmd, shell=True, executable='/bin/bash', check=True)

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

def add_app_to_project(project_path, project_name):
    print("\n" + "="*40)
    print("Django App Creator".center(40))
    print("="*40 + "\n")

    # Validate project path and manage.py
    while True:
        if not os.path.exists(os.path.join(project_path, 'manage.py')):
            print(f"❌ No Django project found at {project_path} (missing manage.py)")
            project_path = input("Enter full path to your Django project folder: ").strip()
        else:
            break

    # Get app name
    while True:
        app_name = input("Enter NEW app name (lowercase, letters, digits, underscores): ").strip()
        try:
            validate_name(app_name, "app")
            break
        except ValueError as e:
            print(f"❌ {e}")

    venv_path = os.path.join(project_path, 'venv')
    if not os.path.exists(venv_path):
        print(f"❌ Virtual environment not found at {venv_path}. Please set up venv before adding apps.")
        return

    try:
        # Create app
        cmd = f"""
        cd '{project_path}' && \
        source {os.path.join(venv_path, 'bin/activate')} && \
        python manage.py startapp {app_name} && \
        deactivate
        """
        print("\n⚙️ Creating app...")
        subprocess.run(cmd, shell=True, executable='/bin/bash', check=True)

        print(f"\n✅ Successfully created app '{app_name}'")

        # Modify settings.py INSTALLED_APPS
        settings_path = os.path.join(project_path, project_name, 'settings.py')
        if not os.path.exists(settings_path):
            print(f"❌ settings.py not found at {settings_path}. Cannot update INSTALLED_APPS.")
            return

        with open(settings_path, 'r') as f:
            lines = f.readlines()

        # Find INSTALLED_APPS block
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if re.match(r'^\s*INSTALLED_APPS\s*=\s*\[', line):
                start_idx = i
                break

        if start_idx == -1:
            print("❌ Could not find INSTALLED_APPS in settings.py")
            return

        # Find closing bracket of INSTALLED_APPS
        for j in range(start_idx, len(lines)):
            if ']' in lines[j]:
                end_idx = j
                break

        if end_idx == -1:
            print("❌ Could not find the end of INSTALLED_APPS list in settings.py")
            return

        # Extract current apps inside INSTALLED_APPS
        current_apps = []
        for k in range(start_idx+1, end_idx):
            app_line = lines[k].strip().strip(',').strip("'\"")
            if app_line:
                current_apps.append(app_line)

        print("\nCurrent apps in INSTALLED_APPS:")
        for idx, app in enumerate(current_apps, 1):
            print(f"{idx}. {app}")

        # Ask user where to insert new app
        position = None
        if current_apps:
            print(f"\nWhere do you want to add '{app_name}'?")
            print("1. Above all existing apps")
            print("2. Below all existing apps")
            print("3. At a specific position")
            choice = input("Choose option (1/2/3): ").strip()

            if choice == '1':
                position = 0
            elif choice == '2':
                position = len(current_apps)
            elif choice == '3':
                pos_input = input(f"Enter position (1 to {len(current_apps)}): ").strip()
                if pos_input.isdigit() and 1 <= int(pos_input) <= len(current_apps):
                    position = int(pos_input) - 1
                else:
                    print("Invalid position, will add at the end.")
                    position = len(current_apps)
            else:
                print("Invalid choice, will add at the end.")
                position = len(current_apps)
        else:
            position = 0

        # Insert the new app
        current_apps.insert(position, app_name)

        # Rebuild INSTALLED_APPS block lines
        new_installed_apps_lines = ['INSTALLED_APPS = [\n']
        for app in current_apps:
            new_installed_apps_lines.append(f"    '{app}',\n")
        new_installed_apps_lines.append(']\n')

        # Replace old INSTALLED_APPS block
        lines = lines[:start_idx] + new_installed_apps_lines + lines[end_idx+1:]

        with open(settings_path, 'w') as f:
            f.writelines(lines)

        print(f"\n✅ Added '{app_name}' to INSTALLED_APPS in settings.py")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to create app: {e}")


def update_dirs_in_templates(settings_path, app_name=None):
    """Update the TEMPLATES DIRS setting in Django settings.py without creating folders and without duplicates."""
    with open(settings_path, 'r') as f:
        content = f.read()

    # Ensure 'import os' exists at the top
    if not re.search(r'^import\s+os\s*$', content, re.MULTILINE):
        content = 'import os\n' + content

    # Regex pattern to find the DIRS list inside TEMPLATES
    templates_pattern = re.compile(
        r'(TEMPLATES\s*=\s*\[\s*\{[^}]*?["\']DIRS["\']\s*:\s*\[)([^\]]*)(\])',
        re.DOTALL
    )

    # Build the DIRS path
    if app_name:
        new_dir = f"os.path.join(BASE_DIR, '{app_name}', 'templates')"
    else:
        new_dir = "os.path.join(BASE_DIR, 'templates')"

    if templates_pattern.search(content):
        def replace_dirs(match):
            existing_dirs = match.group(2).strip()
            if existing_dirs:
                existing_list = [dir.strip() for dir in existing_dirs.split(',') if dir.strip()]
            else:
                existing_list = []

            if new_dir not in existing_list:
                existing_list.append(new_dir)

            return f"{match.group(1)} {', '.join(existing_list)} {match.group(3)}"

        new_content = templates_pattern.sub(replace_dirs, content)
    else:
        # Add new TEMPLATES block if not found
        new_content = content.replace(
            'TEMPLATES = [',
            'TEMPLATES = [\n    {\n        "BACKEND": "django.template.backends.django.DjangoTemplates",\n'
            f'        "DIRS": [{new_dir}],\n'
            '        "APP_DIRS": True,\n'
            '        "OPTIONS": {\n'
            '            "context_processors": [\n'
            '                "django.template.context_processors.debug",\n'
            '                "django.template.context_processors.request",\n'
            '                "django.contrib.auth.context_processors.auth",\n'
            '                "django.contrib.messages.context_processors.messages",\n'
            '            ],\n'
            '        },\n'
            '    },'
        )

    with open(settings_path, 'w') as f:
        f.write(new_content)

    print("✅ Successfully updated TEMPLATES DIRS configuration (no duplicates)")
    return True



def main():
    print("\n" + "="*50)
    print("Django Project Utility".center(50))
    print("="*50)

    while True:
        print("\nChoose an option:")
        print("1. Create a new Django project")
        print("2. Add a new app to an existing Django project")
        print("3. Add templates folder and configure settings.py")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '1':
            # Create new project flow
            while True:
                project_name = input("\nEnter project name (e.g., my_project): ").strip()
                try:
                    validate_name(project_name)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                base_path = input("\nEnter absolute folder path where to create the project: ").strip()
                if not os.path.isabs(base_path):
                    print("❌ Please enter a valid absolute path.")
                    continue

                if not os.path.exists(base_path):
                    create_folder = input(f"Folder does not exist: {base_path}\nCreate it? (y/n): ").strip().lower()
                    if create_folder == 'y':
                        try:
                            os.makedirs(base_path)
                            print(f"✅ Created folder: {base_path}")
                        except Exception as e:
                            print(f"❌ Could not create folder: {e}")
                            continue
                    else:
                        continue

                if not os.path.isdir(base_path):
                    print("❌ The path is not a folder. Try again.")
                    continue

                break

            project_path = os.path.join(base_path, project_name)
            try:
                os.makedirs(project_path, exist_ok=False)
            except FileExistsError:
                print(f"❌ Project folder already exists: {project_path}")
                continue

            if create_traditional_project(project_path, project_name):
                print(f"\n✅ Project created at:\n{project_path}")
                print("Next steps:")
                print(f"cd {project_path}")
                print("source venv/bin/activate")
                print("python manage.py startapp my_app")
                print("python manage.py runserver")
            else:
                print("❌ Project creation failed")

        elif choice == '2':
            # Add app flow
            project_path = input("\nEnter full path to your Django project (where manage.py is): ").strip()
            project_path = os.path.normpath(project_path)

            project_name = input("Enter your Django project name (folder inside project path): ").strip()

            add_app_to_project(project_path, project_name)

        elif choice == '3':
            # Add templates folder flow
            project_path = input("\nEnter full path to your Django project (where manage.py is): ").strip()
            project_path = os.path.normpath(project_path)

            project_name = input("Enter your Django project name (folder inside project path): ").strip()
            settings_path = os.path.join(project_path, project_name, 'settings.py')
    
            if not os.path.exists(settings_path):
                print(f"❌ settings.py not found at {settings_path}")
                continue
    
            app_name = input("Enter app name to add its templates folder (leave empty for project templates only): ").strip()
            if app_name:
                try:
                    validate_name(app_name, "app")
                except ValueError as e:
                    print(f"❌ {e}")
                    continue
    
            update_dirs_in_templates(settings_path, app_name if app_name else None)
    
            # Create templates folders
            templates_path = os.path.join(project_path, 'templates')
            os.makedirs(templates_path, exist_ok=True)
            print(f"✅ Created templates folder at: {templates_path}")
    
            if app_name:
                app_templates_path = os.path.join(project_path, app_name, 'templates')
                os.makedirs(app_templates_path, exist_ok=True)
                print(f"✅ Created app templates folder at: {app_templates_path}")

        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()