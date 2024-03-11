import logging  # Importing the logging module for logging errors and messages

from os import path as ospath, environ  # Importing os.path and os.environ modules for file and environment operations
from subprocess import run as srun  # Importing subprocess.run for running shell commands
from requests import get as rget  # Importing requests.get for making HTTP requests
from dotenv import load_dotenv  # Importing dotenv.load_dotenv for loading environment variables from a .env file

# Check if 'log.txt' file exists, if yes, truncate it to zero length
if ospath.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

# Configure the logging module to log messages to 'log.txt' file and console
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

# Get the URL of the configuration file from the environment variable
CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL', None)

try:
    # Check if the length of CONFIG_FILE_URL is zero, if yes, raise TypeError
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        # Make an HTTP GET request to the configuration file URL
        res = rget(CONFIG_FILE_URL)
        # Check if the status code is 200, if yes, write the content to 'config.env' file
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
            # Log an error message if the status code is not 200
            logging.error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        # Log an error message with the exception details
        logging.error(f"CONFIG_FILE_URL: {e}")
except TypeError:
    # Do nothing if TypeError is raised
    pass

# Load the environment variables from 'config.env' file
load_dotenv('config.env', override=True)

# Get the URL of the upstream repository from the environment variable
UPSTREAM_REPO = environ.get('UPSTREAM_REPO', None)

try:
    # Check if the length of UPSTREAM_REPO is zero, if yes, raise TypeError
    if len(UPSTREAM_REPO) == 0:
