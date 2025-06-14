import os
import subprocess
import requests
from getpass import getpass

# GitHub Login Function
def github_login():
    username = input("GitHub username: ")
    token = getpass("GitHub Personal Access Token: ")  # Not password, but PAT

    # Test authentication
    response = requests.get('https://api.github.com/user', auth=(username, token))
    if response.status_code == 200:
        print(f"Login successful! Welcome {response.json()['login']}")
        return username, token
    else:
        print("❌ Failed to login. Check your username and token.")
        return None, None

# GitHub Upload Automation
def upload_repository(username, token):
    # Ask for local folder path
    local_repo_path = input("Enter the full path to your local project folder: ").strip()

    # Automatically use the folder name as repo name
    repo_name = os.path.basename(local_repo_path.rstrip('/'))
    print(f"Repository name will be: {repo_name}")

    # Create GitHub repository via API
    create_repo_url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    data = {"name": repo_name}

    response = requests.post(create_repo_url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"✅ Repository '{repo_name}' created successfully on GitHub.")
    elif response.status_code == 422:
        print(f"⚠️ Repository '{repo_name}' already exists. Skipping creation.")
    else:
        print(f"❌ Failed to create repository: {response.json()}")
        return

    # Git operations
    os.chdir(local_repo_path)

    # Initialize git if not already a repo
    if not os.path.exists(os.path.join(local_repo_path, ".git")):
        subprocess.run(["git", "init"])

    # Remove existing origin if needed
    subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)

    # Set remote origin
    subprocess.run(["git", "remote", "add", "origin", f"git@github.com:{username}/{repo_name}.git"])

    # Add, commit, push
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Initial commit"])
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "push", "-u", "origin", "main"])

    print("✅ Project pushed successfully to GitHub.")

if __name__ == "__main__":
    username, token = github_login()
    if username and token:
        upload_repository(username, token)
