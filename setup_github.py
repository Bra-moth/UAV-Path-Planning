#!/usr/bin/env python3
"""
GitHub Repository Setup Script for UAV Path Planning Demo
This script helps create and configure the demo repository on GitHub
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def check_git_installed():
    """Check if git is installed"""
    result = run_command("git --version")
    if not result:
        print("Git is not installed. Please install Git first.")
        return False
    print(f"Git version: {result}")
    return True

def check_github_cli_installed():
    """Check if GitHub CLI is installed"""
    result = run_command("gh --version")
    if not result:
        print("GitHub CLI is not installed. Please install GitHub CLI first.")
        print("Visit: https://cli.github.com/")
        return False
    print(f"GitHub CLI version: {result}")
    return True

def setup_repository():
    """Set up the GitHub repository"""
    print("Setting up UAV Path Planning Demo Repository...")
    
    # Check prerequisites
    if not check_git_installed():
        return False
    
    if not check_github_cli_installed():
        return False
    
    # Get repository name from user
    repo_name = input("Enter the desired repository name (e.g., uav-path-planning-demo): ").strip()
    if not repo_name:
        repo_name = "uav-path-planning-demo"
    
    # Get repository description
    description = input("Enter repository description (optional): ").strip()
    if not description:
        description = "UAV Path Planning Simulation Demo - A demonstration of UAV path planning and target acquisition simulation"
    
    # Check if user is authenticated with GitHub
    print("Checking GitHub authentication...")
    auth_result = run_command("gh auth status")
    if not auth_result:
        print("Please authenticate with GitHub first:")
        print("Run: gh auth login")
        return False
    
    # Create repository on GitHub
    print(f"Creating repository: {repo_name}")
    create_cmd = f'gh repo create {repo_name} --public --description "{description}"'
    if run_command(create_cmd):
        print(f"Repository created successfully: https://github.com/{run_command('gh api user --jq .login')}/{repo_name}")
    else:
        print("Failed to create repository. Please check your GitHub permissions.")
        return False
    
    # Initialize git repository locally
    print("Initializing local git repository...")
    if not run_command("git init"):
        print("Failed to initialize git repository")
        return False
    
    # Add all files
    print("Adding files to git...")
    if not run_command("git add ."):
        print("Failed to add files")
        return False
    
    # Create initial commit
    print("Creating initial commit...")
    if not run_command('git commit -m "Initial commit: UAV Path Planning Demo"'):
        print("Failed to create commit")
        return False
    
    # Add remote origin
    print("Adding remote origin...")
    remote_url = f"https://github.com/{run_command('gh api user --jq .login')}/{repo_name}.git"
    if not run_command(f"git remote add origin {remote_url}"):
        print("Failed to add remote origin")
        return False
    
    # Push to GitHub
    print("Pushing to GitHub...")
    if not run_command("git push -u origin main"):
        print("Failed to push to GitHub")
        return False
    
    print("\n" + "="*50)
    print("Repository setup completed successfully!")
    print(f"Repository URL: https://github.com/{run_command('gh api user --jq .login')}/{repo_name}")
    print("\nNext steps:")
    print("1. Update the repository URL in README.md")
    print("2. Add any additional documentation")
    print("3. Test the demo locally")
    print("4. Share the repository with others")
    print("="*50)
    
    return True

def main():
    """Main function"""
    print("UAV Path Planning Demo - GitHub Repository Setup")
    print("="*50)
    
    # Check if we're in the demo repository directory
    if not os.path.exists("src/demo_simulation.py"):
        print("Error: Please run this script from the demo_repository directory")
        print("Current directory:", os.getcwd())
        return
    
    # Setup repository
    if setup_repository():
        print("\nSetup completed successfully!")
    else:
        print("\nSetup failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 