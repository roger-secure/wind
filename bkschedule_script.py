import schedule
import time
import subprocess

def download_xml():
    # Remove the existing IDV60920.xml file if it exists
    subprocess.run(['rm', '-f', 'IDV60920.xml'])
    
    # Download the IDV60920.xml file using lftp
    subprocess.run(['lftp', '-c', "open -e 'get /anon/gen/fwo/IDV60920.xml' ftp://ftp.bom.gov.au"])

# Schedule the job to run every minute
schedule.every(1).minutes.do(download_xml)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)

