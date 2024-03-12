import subprocess
import schedule

def push_to_github():
    # Check for uncommitted changes
    status = subprocess.run(["git", "status"], capture_output=True, text=True).stdout
    if "nothing to commit, working directory clean" not in status:
        # Uncommitted changes found, proceed with push
        command = "git push origin master"
        subprocess.run(command.split(), check=True)
        print("Successfully pushed changes to GitHub.")
    else:
        print("No uncommitted changes found, skipping push.")

# Schedule the function... (rest of the code)

