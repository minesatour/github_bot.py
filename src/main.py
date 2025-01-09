import os
import subprocess
import json
from github import Github

REPO_FILE = "repositories.json"


# GitHub Authentication
def authenticate_github(token):
    try:
        return Github(token)
    except Exception as e:
        print(f"Authentication failed: {e}")
        exit(1)


# Create Repository
def create_repository(github_instance, repo_name, description=""):
    try:
        user = github_instance.get_user()
        repo = user.create_repo(repo_name, description=description)
        print(f"Repository {repo_name} created successfully.")
        return repo.clone_url
    except Exception as e:
        print(f"Failed to create repository: {e}")
        exit(1)


# Setup Project Structure
def setup_project(repo_name):
    try:
        os.makedirs(f"{repo_name}/src", exist_ok=True)
        os.makedirs(f"{repo_name}/tests", exist_ok=True)
        os.makedirs(f"{repo_name}/docs", exist_ok=True)

        with open(f"{repo_name}/README.md", "w") as f:
            f.write(f"# {repo_name}\n\nDescription of the project.\n\n## Installation\n\n```\npip install -r requirements.txt\n```\n\n## Usage\n\nExplain how to use the script.\n")

        with open(f"{repo_name}/requirements.txt", "w") as f:
            f.write("# Add your dependencies here, e.g.,\n# requests\n# pytest\n")

        with open(f"{repo_name}/.gitignore", "w") as f:
            f.write("__pycache__/\n*.pyc\n")

        print(f"Project structure for {repo_name} created successfully.")
    except Exception as e:
        print(f"Failed to set up project structure: {e}")
        exit(1)


# Save Repository Information
def save_repository_info(repo_name, description, path, clone_url):
    repo_data = {"name": repo_name, "description": description, "path": path, "clone_url": clone_url}
    if os.path.exists(REPO_FILE):
        with open(REPO_FILE, "r") as f:
            repos = json.load(f)
    else:
        repos = []

    repos.append(repo_data)
    with open(REPO_FILE, "w") as f:
        json.dump(repos, f, indent=4)
    print(f"Repository {repo_name} saved to {REPO_FILE}.")


# Load Repository Information
def load_repositories():
    if os.path.exists(REPO_FILE):
        with open(REPO_FILE, "r") as f:
            return json.load(f)
    else:
        return []


# Test Script
def test_script(repo_name):
    try:
        test_file = os.path.join(repo_name, "src", "main.py")
        result = subprocess.run(["python3", test_file], capture_output=True, text=True)
        if result.returncode == 0:
            print("Script ran successfully!")
            return True
        else:
            print(f"Script failed to run. Error:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"Failed to test the script: {e}")
        return False


# Add or Update Script
def add_or_update_script(repo_name, new_code):
    try:
        script_path = os.path.join(repo_name, "src", "main.py")
        with open(script_path, "w") as f:
            f.write(new_code)
        print(f"Script added/updated at {script_path}.")
    except Exception as e:
        print(f"Failed to add or update the script: {e}")


# Push to GitHub
def push_to_github(repo_path, clone_url):
    try:
        os.chdir(repo_path)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Update script"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changes pushed to GitHub successfully.")
    except Exception as e:
        print(f"Failed to push changes: {e}")
        exit(1)


# Main Function
def main():
    token = input("Enter your GitHub Personal Access Token (PAT): ").strip()
    github = authenticate_github(token)

    while True:
        print("\nMenu:")
        print("1. Create a new repository")
        print("2. Add/Update code in an existing repository")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            repo_name = input("Enter the repository name: ").strip()
            description = input("Enter a description for the repository (optional): ").strip()

            print("\nCreating repository on GitHub...")
            clone_url = create_repository(github, repo_name, description)

            print("\nSetting up the project structure locally...")
            setup_project(repo_name)

            print("\nSaving repository information...")
            save_repository_info(repo_name, description, os.path.abspath(repo_name), clone_url)

            print("\nRepository setup complete.")

        elif choice == "2":
            repos = load_repositories()
            if not repos:
                print("No repositories found. Please create a repository first.")
                continue

            print("\nExisting Repositories:")
            for i, repo in enumerate(repos):
                print(f"{i + 1}. {repo['name']}")

            repo_choice = int(input("Select a repository by number: ").strip()) - 1
            if 0 <= repo_choice < len(repos):
                repo_name = repos[repo_choice]["name"]
                repo_path = repos[repo_choice]["path"]
                clone_url = repos[repo_choice]["clone_url"]

                print("\nEnter the new script code (end with EOF):")
                lines = []
                while True:
                    line = input()
                    if line == "EOF":
                        break
                    lines.append(line)
                new_code = "\n".join(lines)

                print("\nAdding or updating the script...")
                add_or_update_script(repo_path, new_code)

                print("\nTesting the script...")
                if test_script(repo_path):
                    print("\nPushing changes to GitHub...")
                    push_to_github(repo_path, clone_url)
                else:
                    print("Script failed testing. Please fix the issues before pushing.")

            else:
                print("Invalid choice. Please try again.")

        elif choice == "3":
            print("Exiting.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
