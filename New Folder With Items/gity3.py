import subprocess
import schedule


def push_to_github():
    """
    Checks for uncommitted changes and pushes to GitHub if necessary.
    """

    # Check for uncommitted changes
    status = subprocess.run(["git", "status"], capture_output=True, text=True).stdout
    if "nothing to commit, working directory clean" not in status:
        # Uncommitted changes found, proceed with push
        print("Uncommitted changes detected. Pushing to GitHub...")
        command = "git push origin master"
        subprocess.run(command.split(), check=True)
        print("Successfully pushed changes to GitHub.")
    else:
        print("No uncommitted changes found, skipping push.")


# Schedule the function to run every minute (replace 60 with desired interval in seconds)
schedule.every(60).seconds.do(push_to_github)

while True:
    schedule.run_pending()
    schedule.sleep(1)

