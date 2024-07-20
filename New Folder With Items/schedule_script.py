import schedule
import time
import subprocess
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Configurable parameters
FILE_NAME = 'IDV60920.xml'
FTP_URL = 'ftp://ftp.bom.gov.au'
FTP_PATH = f'/anon/gen/fwo/{FILE_NAME}'

def download_xml():
    try:
        # Remove the existing file if it exists
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
            logging.info(f"Removed existing {FILE_NAME}")
        
        # Download the file using lftp
        result = subprocess.run(['lftp', '-c', f"open -e 'get {FTP_PATH}' {FTP_URL}"], capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info(f"Successfully downloaded {FILE_NAME}")
        else:
            logging.error(f"Failed to download {FILE_NAME}. Error: {result.stderr}")
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

# Schedule the job to run every minute
schedule.every(1).minutes.do(download_xml)

# Run the scheduler
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Script stopped by user")