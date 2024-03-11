# Import necessary modules
from time import sleep  # Import sleep from time module to introduce delay
from requests import get as rget  # Import get function from requests module and rename it as rget
from os import environ  # Import environ from os module to access environment variables
from logging import error as logerror  # Import error function from logging module and rename it as logerror

# Assign the base URL of the bot to the variable BASE_URL, using the environment variable BASE_URL_OF_BOT
BASE_URL = environ.get('BASE_URL_OF_BOT', None)

# Check if BASE_URL is not empty, if so, remove any trailing slashes
try:
    if len(BASE_URL) == 0:
        raise TypeError  # Raise a TypeError if BASE_URL is empty
    BASE_URL = BASE_URL.rstrip("/")  # Remove trailing slashes
except TypeError:
    BASE_URL = None  # If a TypeError is raised, set BASE_URL to None

# Assign the port number to the variable PORT, using the environment variable PORT
PORT = environ.get('PORT', None)

# Check if both BASE_URL and PORT are not None
if PORT is not None and BASE_URL is not None:
    while True:  # Start an infinite loop
        try:
            # Send a GET request to the base URL and check its status code
            rget(BASE_URL).status_code
            sleep(600)  # Wait for 600 seconds (10 minutes) before sending the next request
        except Exception as e:  # If an exception occurs
            logerror(f"alive.py: {e}")  # Log the error message
            sleep(2)  # Wait for 2 seconds before continuing
            continue  # Continue to the next iteration of the loop
