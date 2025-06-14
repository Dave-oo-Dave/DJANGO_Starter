import os
import subprocess
import webbrowser
import time
import getpass

def ensure_django_installed(project_path):
    """Ensure Django is installed in the virtual environment"""
    venv_path = os.path.join(project_path, 'venv')
    if not os.path.exists(venv_path):
        raise FileNotFoundError(f"Virtual environment not found at {venv_path}")
    
    check_django_cmd = [
        os.path.join(venv_path, 'bin', 'python'),
        '-c',
        "import django; print(django.__version__)"
    ]

    try:
        subprocess.run(check_django_cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print("Installing Django...")
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        install_cmd = [pip_path, 'install', 'django']
        try:
            subprocess.run(install_cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Django: {e}")
            return False

def list_existing_users(project_path, project_name):
    """List existing superusers in the database"""
    venv_path = os.path.join(project_path, 'venv')
    python_path = os.path.join(venv_path, 'bin', 'python')

    list_users_script = f"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
for user in users:
    print(user.username)
"""

    result = subprocess.run([python_path, '-c', list_users_script], cwd=project_path, capture_output=True, text=True)
    user_list = result.stdout.strip().split('\n')
    if user_list == ['']:
        print("\n📜 No users found in the database.\n")
    else:
        print("\n📜 Existing users in the database:\n")
        for user in user_list:
            print(user)
        print("\n")

def get_superuser_details():
    """Collect superuser details from user"""
    print("Please enter superuser details:")
    username = input("Username: ").strip()
    while not username:
        print("Username cannot be empty")
        username = input("Username: ").strip()

    email = input("Email (optional, press Enter to skip): ").strip()

    while True:
        password = getpass.getpass("Password: ").strip()
        password_confirm = getpass.getpass("Confirm Password: ").strip()
        if password == password_confirm:
            break
        print("❌ Passwords don't match. Please try again.")

    return username, email, password

def check_user_exists(project_path, project_name, username):
    """Check if a user already exists"""
    venv_path = os.path.join(project_path, 'venv')
    python_path = os.path.join(venv_path, 'bin', 'python')

    check_user_script = f"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
exists = User.objects.filter(username='{username}').exists()
print('EXISTS' if exists else 'NOT_EXISTS')
"""

    result = subprocess.run([python_path, '-c', check_user_script], cwd=project_path, capture_output=True, text=True)
    status = result.stdout.strip()
    return status == 'EXISTS'

def create_or_update_superuser(project_path, project_name, username, email, password):
    """Create or update Django superuser"""
    venv_path = os.path.join(project_path, 'venv')
    python_path = os.path.join(venv_path, 'bin', 'python')

    try:
        if check_user_exists(project_path, project_name, username):
            print("⚙️ User already exists. Updating password...")
            update_password_script = f"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='{username}')
user.set_password('{password}')
user.save()

print("✅ Password updated successfully")
"""
            subprocess.run([python_path, '-c', update_password_script], cwd=project_path, check=True)
            return True
        else:
            print("👑 Creating superuser...")
            create_cmd = [
                python_path,
                'manage.py',
                'createsuperuser',
                '--username', username,
                '--email', email if email else '',
                '--noinput'
            ]
            subprocess.run(create_cmd, cwd=project_path, check=True)

            set_password_script = f"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='{username}')
user.set_password('{password}')
user.save()

print("✅ Superuser created successfully")
"""
            subprocess.run([python_path, '-c', set_password_script], cwd=project_path, check=True)
            return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating or updating superuser: {e}")
        return False

def delete_user(project_path, project_name, username):
    """Delete a user by username"""
    venv_path = os.path.join(project_path, 'venv')
    python_path = os.path.join(venv_path, 'bin', 'python')

    delete_user_script = f"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    user = User.objects.get(username='{username}')
    user.delete()
    print('✅ User deleted successfully')
except User.DoesNotExist:
    print('❌ User does not exist')
"""

    subprocess.run([python_path, '-c', delete_user_script], cwd=project_path)

def run_server_and_open_admin(project_path):
    """Run development server and open admin panel"""
    venv_path = os.path.join(project_path, 'venv')
    python_path = os.path.join(venv_path, 'bin', 'python')

    try:
        server_process = subprocess.Popen(
            [python_path, 'manage.py', 'runserver'],
            cwd=project_path
        )

        time.sleep(3)
        webbrowser.open("http://127.0.0.1:8000/admin/")

        print("\n✅ Admin panel opened in your browser. Please login with your superuser credentials.")
        print("Press Ctrl+C in this terminal when you're done to stop the server.")

        server_process.wait()

    except Exception as e:
        print(f"❌ Error running server: {e}")
        if 'server_process' in locals():
            server_process.terminate()

def main():
    print("\n" + "=" * 50)
    print("Django Superuser Manager".center(50))
    print("=" * 50)

    while True:
        project_path = input("\nEnter full path to your Django project: ").strip()
        if os.path.exists(project_path):
            if os.path.exists(os.path.join(project_path, 'manage.py')):
                break
            print("❌ No manage.py found in this directory - not a Django project")
        else:
            print("❌ Directory does not exist")

    project_name = input("\nEnter your Django project name (folder that contains settings.py): ").strip()

    try:
        print("\n🔌 Checking Django installation...")
        if not ensure_django_installed(project_path):
            print("❌ Failed to setup Django environment")
            return

        while True:
            print("\nWhat would you like to do?")
            print("[1] List existing users")
            print("[2] Create or update superuser")
            print("[3] Delete a user")
            print("[4] Run development server and open admin panel")
            print("[5] Exit")

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == '1':
                list_existing_users(project_path, project_name)
            elif choice == '2':
                username, email, password = get_superuser_details()
                if create_or_update_superuser(project_path, project_name, username, email, password):
                    print("\n✅ Superuser created or updated successfully")
            elif choice == '3':
                username = input("\nEnter the username to delete: ").strip()
                if username:
                    delete_user(project_path, project_name, username)
                else:
                    print("❌ Username cannot be empty")
            elif choice == '4':
                print("\n🚀 Starting development server...")
                run_server_and_open_admin(project_path)
            elif choice == '5':
                print("\n👋 Exiting...")
                break
            else:
                print("❌ Invalid choice. Please select from 1 to 5.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("\nScript completed")

if __name__ == "__main__":
    main()
