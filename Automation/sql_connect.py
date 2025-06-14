import os
import subprocess
import re
import getpass

def run_migrations(project_path):
    """Run Django migrations after successful configuration"""
    print("\n🔄 Running Django Migrations...")
    
    makemigrations_command = ["python", "manage.py", "makemigrations"]
    print(f"Running: {' '.join(makemigrations_command)} in {project_path}")
    makemigrations_process = subprocess.run(
        makemigrations_command,
        cwd=project_path,
        shell=False,
        capture_output=True,
        text=True
    )
    print(makemigrations_process.stdout)
    if makemigrations_process.stderr:
        print(f"\n❌ Makemigrations errors:\n{makemigrations_process.stderr}")
        return # Stop if makemigrations fails

    migrate_command = ["python", "manage.py", "migrate"]
    print(f"Running: {' '.join(migrate_command)} in {project_path}")
    migrate_process = subprocess.run(
        migrate_command,
        cwd=project_path,
        shell=False,
        capture_output=True,
        text=True
    )
    print(migrate_process.stdout)
    if migrate_process.stderr:
        print(f"\n❌ Migration errors:\n{migrate_process.stderr}")
    else:
        print("\n✅ Migrations completed successfully!")

def auto_activate_and_configure():
    print("\n🚀 Django Project Configuration & Migration Setup 🚀")
    
    project_path = input("Enter full path to your Django project: ").strip()
    if not os.path.exists(project_path):
        print(f"❌ Path not found: {project_path}")
        return
    
    venv_path = None
    for venv_name in ['venv', '.venv', 'env']:
        possible_path = os.path.join(project_path, venv_name)
        if os.path.exists(possible_path):
            venv_path = possible_path
            break
    
    if not venv_path:
        print("\n❌ No virtualenv found in project! Please create one (e.g., `python3 -m venv venv`)")
        return
    
    print(f"\n🔧 Activating virtual environment and installing dependencies at {venv_path}")
    commands = [
        f"source {os.path.join(venv_path, 'bin', 'activate')}",
        "pip install --upgrade pip",
        "pip install Django PyMySQL",
        '''python -c "import pymysql; print(f'\\n✅ PyMySQL {pymysql.__version__} ready!')"''',
        '''python -c "import django; print(f'\\n✅ Django {django.VERSION} ready!')"'''
    ]
    
    setup_process = subprocess.run(
        " && ".join(commands),
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True
    )
    print(setup_process.stdout)
    if setup_process.stderr:
        print(f"\n❌ Setup errors:\n{setup_process.stderr}")
        return
        
    project_name = os.path.basename(project_path)
    settings_path = os.path.join(project_path, project_name, "settings.py")

    if not os.path.exists(settings_path):
        print(f"\n❌ settings.py not found at: {settings_path}. Please check your project structure.")
        return

    print("\n📝 Database Configuration")
    print("-----------------------")
    
    db_config = {
        'NAME': input("Database name (required): "),
        'USER': input("Database user (required): "),
        'PASSWORD': getpass.getpass("Database password (input hidden): "),
        'HOST': input("Host [127.0.0.1]: ") or "127.0.0.1",
        'PORT': input("Port [3306]: ") or "3306",
    }

    if not all([db_config['NAME'], db_config['USER']]):
        print("\n❌ Database name and user are required!")
        return

    config_template = f"""
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{db_config['NAME']}',
        'USER': '{db_config['USER']}',
        'PASSWORD': '{db_config['PASSWORD']}',
        'HOST': '{db_config['HOST']}',
        'PORT': '{db_config['PORT']}',
        'OPTIONS': {{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }},
    }}
}}
"""

    backup_path = settings_path + ".bak"
    try:
        with open(settings_path, 'r') as f:
            original = f.read()
        with open(backup_path, 'w') as b:
            b.write(original)
        
        # Find where DATABASES starts and where it ends
        match = re.search(r"DATABASES\s*=\s*{.*?}(?=\s*#|\s*\w+\s*=|$)", original, re.DOTALL)

        if match:
            start, end = match.span()
            updated_content = original[:start] + config_template + original[end:]
        else:
            updated_content = original + "\n" + config_template + "\n"

        with open(settings_path, 'w') as f:
            f.write(updated_content)

        print("\n✅ Database configured successfully!")
    except Exception as e:
        print(f"\n❌ Error configuring database: {e}")
        return

    init_py_path = os.path.join(project_path, project_name, "__init__.py")
    pymysql_import_line = "import pymysql"
    pymysql_install_line = "pymysql.install_as_MySQLdb()"

    if os.path.exists(init_py_path):
        try:
            with open(init_py_path, 'r+') as f:
                content = f.read()
                
                has_import = pymysql_import_line in content
                has_install = pymysql_install_line in content

                if not has_import and not has_install:
                    f.seek(0)
                    f.truncate(0)
                    f.write(f"{pymysql_import_line}\n{pymysql_install_line}\n\n{content.strip()}")
                    print(f"\n✅ Added PyMySQL import and installation to: {init_py_path}")
                elif has_import and not has_install:
                    f.seek(0)
                    f.truncate(0)
                    updated_content = content.replace(pymysql_import_line, f"{pymysql_import_line}\n{pymysql_install_line}")
                    f.write(updated_content.strip())
                    print(f"\n✅ Added PyMySQL installation to existing import in: {init_py_path}")
                else:
                    print(f"\nℹ️ PyMySQL import and installation already present in: {init_py_path}")

        except Exception as e:
            print(f"\n⚠️ Could not automatically add PyMySQL import to {init_py_path}: {e}")
            print("Please manually add the following lines to your project's __init__.py file:")
            print(f"    {pymysql_import_line}")
            print(f"    {pymysql_install_line}")
    else:
        print(f"\n⚠️ Could not find __init__.py at {init_py_path}.")
        print("Please manually create or add the following lines to your project's main __init__.py file:")
        print(f"    {pymysql_import_line}")
        print(f"    {pymysql_install_line}")

    run_migrations(project_path)

if __name__ == "__main__":
    auto_activate_and_configure()