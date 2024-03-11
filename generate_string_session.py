from pyrogram import Client # Import the Client class from the pyrogram library

# Define the API key and hash as variables
API_KEY = int(input("Enter API KEY: "))
API_HASH = input("Enter API HASH: ")

# Create a new in-memory Client instance with the specified API key and hash
with Client(':memory:', api_id=API_KEY, api_hash=API_HASH) as app:
    # Export the session string for the Client instance
    print(app.export_session_string())
