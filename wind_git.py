import subprocess

# Clone the repository
subprocess.run(["git", "clone", "https://github.com/roger-secure/wind.git"])

# Navigate into the cloned directory
repo_dir = "wind"
subprocess.run(["cd", repo_dir], shell=True)

# Add changes
subprocess.run(["git", "add", "."])

# Commit changes
commit_message = "chart update"
subprocess.run(["git", "commit", "-m", commit_message])

# Push changes to origin main
subprocess.run(["git", "push", "origin", "main"])

