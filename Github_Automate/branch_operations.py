import requests
import subprocess
import os
from getpass import getpass

def github_login():
    username = input("GitHub username: ")
    token = getpass("GitHub Personal Access Token: ")
    response = requests.get('https://api.github.com/user', auth=(username, token))
    if response.status_code == 200:
        print(f"Login successful! Welcome {response.json()['login']}")
        return username, token
    else:
        print("Failed to login. Check your username and token.")
        return None, None

def list_repos(username, token):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url, auth=(username, token))
        if response.status_code != 200:
            print("Failed to fetch repositories.")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    for idx, repo in enumerate(repos, 1):
        print(f"{idx}. {repo['name']}")
    return repos

def choose_repo(repos):
    choice = input("Enter the number of the repo you want to work with: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(repos):
            return repos[choice - 1]['name']
    except ValueError:
        pass
    print("Invalid choice.")
    return None

def check_git_repo(path):
    if not os.path.isdir(path):
        print("Path does not exist or is not a directory.")
        return False
    if not os.path.isdir(os.path.join(path, '.git')):
        print("This is not a git repository (no .git folder found).")
        return False
    return True

def run_git_command(cmd_list, cwd):
    result = subprocess.run(cmd_list, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        return False, result.stderr.strip()
    return True, result.stdout.strip()

def create_branch(branch_name, repo_path):
    print(f"Creating new branch '{branch_name}'...")
    success, _ = run_git_command(['git', 'checkout', '-b', branch_name], repo_path)
    return success

def commit_all_changes(repo_path, commit_msg="Automated commit"):
    # Check if there are any changes to commit
    success, status_output = run_git_command(['git', 'status', '--porcelain'], repo_path)
    if not success:
        return False
    if not status_output.strip():
        print("No changes to commit.")
        return True

    # Add all changes
    success, add_output = run_git_command(['git', 'add', '.'], repo_path)
    if not success:
        print("Failed to add changes.")
        return False

    # Commit
    success, commit_output = run_git_command(['git', 'commit', '-m', commit_msg], repo_path)
    if not success:
        if "nothing to commit" in commit_output.lower():
            print("Nothing to commit after adding changes.")
            return True
        else:
            print(f"Failed to commit: {commit_output}")
            return False
    print(commit_output)
    return True

def push_branch(branch_name, repo_path):
    print(f"Pushing branch '{branch_name}' to remote...")

    # Commit changes before push
    if not commit_all_changes(repo_path):
        print("Aborting push due to commit failure.")
        return

    # Push the branch
    success, push_output = run_git_command(['git', 'push', '-u', 'origin', branch_name], repo_path)
    if success:
        print(push_output)
    else:
        print(f"Failed to push branch: {push_output}")

def delete_branch(branch_name, repo_path):
    print(f"Deleting local branch '{branch_name}'...")
    run_git_command(['git', 'branch', '-d', branch_name], repo_path)
    print(f"Deleting remote branch '{branch_name}'...")
    run_git_command(['git', 'push', 'origin', '--delete', branch_name], repo_path)

def main():
    username, token = github_login()
    if not username:
        return

    repos = list_repos(username, token)
    if not repos:
        print("No repositories found.")
        return

    repo_name = choose_repo(repos)
    if not repo_name:
        return

    repo_path = input(f"Enter the local path for repo '{repo_name}': ").strip()
    if not check_git_repo(repo_path):
        return

    print("\nOptions:\n1. Create a new branch\n2. Push an existing branch\n3. Delete a branch")
    option = input("Choose an option (1/2/3): ").strip()

    if option == '1':
        branch_name = input("Enter the new branch name: ").strip()
        if create_branch(branch_name, repo_path):
            print("Branch created locally.")
            push_now = input("Do you want to push it now? (y/n): ").strip().lower()
            if push_now == 'y':
                push_branch(branch_name, repo_path)

    elif option == '2':
        branch_name = input("Enter the branch name to push: ").strip()
        push_branch(branch_name, repo_path)

    elif option == '3':
        branch_name = input("Enter the branch name to delete: ").strip()
        confirm = input(f"Are you sure you want to delete branch '{branch_name}' locally and remotely? (y/n): ").strip().lower()
        if confirm == 'y':
            delete_branch(branch_name, repo_path)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
