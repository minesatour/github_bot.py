GitHub Automation Bot
This script simplifies repository management by allowing users to create and update GitHub repositories directly from the command line. It automates the following tasks:

Creating new repositories on GitHub with a predefined folder structure.
Adding or updating scripts in existing repositories.
Testing the provided code to ensure it runs successfully.
Pushing changes to GitHub only if the code passes the test.
Features
Create Repositories:

Automatically sets up a project structure with folders (src, tests, docs) and essential files (README.md, .gitignore, etc.).
Pushes the initial commit to GitHub.
Update Scripts:

Allows users to add or update scripts in existing repositories.
Tests the script locally to ensure functionality before pushing to GitHub.
Interactive Menu:

Provides an easy-to-use menu for managing repositories and scripts.
Installation
Prerequisites
Python 3.x
Ensure Python is installed on your system. Download Python

Git
Make sure Git is installed and configured. Download Git

GitHub Personal Access Token (PAT)

Generate a token with repo permissions.
Create a GitHub PAT.
Setup
Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/github-automation-bot.git  
cd github-automation-bot  
Install dependencies:

bash
Copy code
pip install PyGithub  
Make the script executable:

bash
Copy code
chmod +x github_bot.py  
Usage
Run the script:

bash
Copy code
python github_bot.py  
Follow the interactive menu options:

Option 1: Create a new repository. Provide a name, description, and the script will handle the rest.
Option 2: Add or update code in an existing repository. Paste the new code, and the bot will test it before pushing to GitHub.
Option 3: Exit the program.
To end the code input while using Option 2, type EOF on a new line.

Folder Structure
When creating a new repository, the following structure is set up:

bash
Copy code
repo_name/  
├── src/            # Place your main scripts here.  
│   └── main.py  
├── tests/          # Add your test cases here.  
│   └── test_main.py  
├── docs/           # Documentation folder.  
├── README.md       # Project description.  
├── requirements.txt # Dependencies for the project.  
├── .gitignore      # Ignored files and folders.  
Testing
The script automatically runs the provided code using Python.
If the test fails, it outputs the error for debugging.
If successful, the code is pushed to GitHub.
