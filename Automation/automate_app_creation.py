import os
import subprocess
import re

def is_valid_name(name, name_type="app"):
    """Validate project or app names"""
    if not name:
        return False, f"{name_type} name cannot be empty"
    
    if name_type == "app":
        if not re.match(r'^[a-z][a-z0-9_]*$', name):
            return False, "App names must be lowercase, start with a letter, and only contain letters, numbers, or underscores"
    else:  # project name
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
            return False, "Project names should start with a letter and only contain letters, numbers, or underscores"
    
    python_keywords = {'email', 'admin', 'test', 'api', 'user'}  # Common conflicts
    if name.lower() in python_keywords:
        return False, f"'{name}' is a common conflict name"
    
    return True, ""

def create_django_app():
    print("\n" + "="*40)
    print("Django App Creator".center(40))
    print("="*40 + "\n")
    
    # --- STEP 1: Get Project Location ---
    while True:
        project_path = input("➤ Enter FULL PATH to your Django project (where manage.py is): ").strip()
        project_path = os.path.normpath(project_path)
        
        if os.path.exists(os.path.join(project_path, 'manage.py')):
            break
        print(f"❌ Error: No Django project found at {project_path} (missing manage.py)")
        print("Example: /Users/yourname/Desktop/MyProject\n")

    # --- STEP 2: Get Project Name ---
    while True:
        project_name = input("\n➤ Enter your Django PROJECT name (from startproject): ").strip()
        valid, msg = is_valid_name(project_name, "project")
        if valid: break
        print(f"❌ Invalid project name: {msg}")
        print("Example: 'MySite', 'BlogProject'\n")

    # --- STEP 3: Get App Name ---
    while True:
        app_name = input("\n➤ Enter NEW APP name: ").strip()
        valid, msg = is_valid_name(app_name)
        if valid: break
        print(f"❌ Invalid app name: {msg}")
        print("Examples: 'blog', 'user_profile', 'payment'\n")

    # --- Create App ---
    try:
        cmd = f"""
        cd '{project_path}' && \
        source venv/bin/activate && \
        python manage.py startapp {app_name} && \
        deactivate
        """
        print("\n⚙️ Creating app...")
        subprocess.run(cmd, shell=True, executable='/bin/bash', check=True)
        
        app_path = os.path.join(project_path, app_name)
        print(f"\n✅ Successfully created '{app_name}' in project '{project_name}'!")
        print(f"📍 Location: {app_path}")
        
        print("\nNext steps:")
        print(f"1. Add '{app_name}' to INSTALLED_APPS in {project_name}/settings.py")
        print(f"2. Create your models in {app_name}/models.py")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to create app: {e}")
        print("Possible solutions:")
        print("- Make sure virtual environment is properly set up")
        print("- Check you have Django installed in your venv")
        print("- Verify the project name is correct")

if __name__ == "__main__":
    create_django_app()
    input("\nPress Enter to exit...")