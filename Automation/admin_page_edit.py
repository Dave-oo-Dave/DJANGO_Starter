import os
import subprocess
import sys

def ask_path(prompt):
    while True:
        path = input(prompt).strip()
        if os.path.exists(path):
            return path
        else:
            print("Path does not exist. Try again.")

def activate_venv(project_path):
    possible_venvs = ['venv', 'env', '.venv']
    for venv_name in possible_venvs:
        venv_path = os.path.join(project_path, venv_name)
        if os.path.exists(venv_path):
            if os.name == 'nt':  # Windows
                activate_script = os.path.join(venv_path, 'Scripts', 'activate')
            else:  # Unix
                activate_script = os.path.join(venv_path, 'bin', 'activate')
            if os.path.exists(activate_script):
                return activate_script
    return None

def modify_settings(settings_path, app_name):
    with open(settings_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_installed_apps = False
    inserted_app = False
    in_templates = False
    dirs_updated = False
    os_imported = False

    for line in lines:
        stripped_line = line.strip()

        # Ensure 'import os' is present
        if stripped_line == 'import os':
            os_imported = True

        # Insert app into INSTALLED_APPS
        if 'INSTALLED_APPS' in line and '=' in line:
            in_installed_apps = True
            new_lines.append(line)
            continue

        if in_installed_apps:
            if f'"{app_name}"' in line:
                inserted_app = True  # Already added
            if '"django.contrib.admin"' in line and not inserted_app:
                new_lines.append(f'    "{app_name}",\n')
                inserted_app = True
            if line.strip().startswith(']'):
                in_installed_apps = False
            new_lines.append(line)
            continue

        # Update DIRS properly in TEMPLATES
        if '"DIRS"' in line and not dirs_updated:
            indent = ' ' * (len(line) - len(line.lstrip()))
            new_dirs_line = f'{indent}"DIRS": [\n' \
                            f'{indent}    os.path.join(BASE_DIR, "templates"),\n' \
                            f'{indent}    os.path.join(BASE_DIR, "{app_name}", "templates"),\n' \
                            f'{indent}],\n'
            new_lines.append(new_dirs_line)
            dirs_updated = True
            continue

        new_lines.append(line)

    if not os_imported:
        new_lines.insert(0, "import os\n")

    with open(settings_path, 'w') as f:
        f.writelines(new_lines)

def main():
    print("Django Automation Script")

    project_path = ask_path("Enter the full Django project root path: ")
    project_name = input("Enter the Django project name (the folder containing settings.py): ").strip()
    app_name = input("Enter the Django app name: ").strip()

    activate_script = activate_venv(project_path)
    if not activate_script:
        print("Could not find virtual environment in the project folder. Please activate it manually.")
    else:
        print(f"Virtual environment activate script found at: {activate_script}")
        print("Note: This script won't actually activate the virtualenv inside this Python script since it's a subprocess issue.")
        print("You'll need to run the server manually if you want venv activated properly.")

    # Create templates/admin folder inside app
    app_path = os.path.join(project_path, app_name)
    templates_path = os.path.join(app_path, "templates")
    admin_template_path = os.path.join(templates_path, "admin")

    os.makedirs(admin_template_path, exist_ok=True)
    print(f"Created folder: {admin_template_path}")

    # Ask user for login.html input method
    choice = input("Do you want to (1) provide path to existing login.html or (2) enter the HTML code now? (1/2): ").strip()
    login_html_path = os.path.join(admin_template_path, "login.html")

    if choice == '1':
        source_file = ask_path("Enter the full path of your login.html file: ")
        with open(source_file, 'r') as sf, open(login_html_path, 'w') as lf:
            lf.write(sf.read())
        print(f"Copied login.html to {login_html_path}")
    elif choice == '2':
        print("Enter your login.html code below. End input with a single line containing only 'EOF'")
        lines = []
        while True:
            line = input()
            if line.strip() == 'EOF':
                break
            lines.append(line)
        with open(login_html_path, 'w') as lf:
            lf.write('\n'.join(lines))
        print(f"Saved login.html to {login_html_path}")
    else:
        print("Invalid choice, exiting.")
        sys.exit(1)

    settings_path = os.path.join(project_path, project_name, "settings.py")
    if not os.path.exists(settings_path):
        print(f"Cannot find settings.py at {settings_path}. Exiting.")
        sys.exit(1)

    modify_settings(settings_path, app_name)
    print(f"Modified settings.py at {settings_path}")

    # Run the server
    manage_py = os.path.join(project_path, "manage.py")
    if not os.path.exists(manage_py):
        print(f"Cannot find manage.py at {manage_py}. Exiting.")
        sys.exit(1)

    print("Starting Django development server...")
    subprocess.run([sys.executable, manage_py, "runserver"])

if __name__ == "__main__":
    main()
