import subprocess
import schedule
import time  # Import the time library for sleep functionality

def push_to_github():
    try:
        # No URL needed as SSH key handles authentication
        command = "git push origin master"
        subprocess.run(command.split(), check=True)
        print("Successfully pushed changes to GitHub.")
    except subprocess.CalledProcessError as error:
        print(f"Error pushing to GitHub: {error}")

# Schedule the function to run every minute (replace 60 with desired interval in seconds)
schedule.every(60).seconds.do(push_to_github)

while True:
    schedule.run_pending()
    # Use time.sleep() for the desired delay between checks
    time.sleep(1)  # Sleep for 1 second

