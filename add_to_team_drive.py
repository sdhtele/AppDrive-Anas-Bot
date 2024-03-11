from __future__ import print_function  # Enable print function for Python 2.x

import googleapiclient.discovery, json, progress.bar, glob, sys, argparse, time  # Import required libraries
from google_auth_oauthlib.flow import InstalledAppFlow  # For getting user credentials
from google.auth.transport.requests import Request  # For refreshing credentials
import os, pickle  # For handling files and directories

# Initialize start time
stt = time.time()

# Initialize argparse to parse command-line arguments
parse = argparse.ArgumentParser(
    description='A tool to add service accounts to a shared drive from a folder containing credential files.')

# Define arguments
parse.add_argument('--path', '-p', default='accounts',
                   help='Specify an alternative path to the service accounts folder.')
parse.add_argument('--credentials', '-c', default='./credentials.json',
                   help='Specify the relative path for the credentials file.')
parse.add_argument('--yes', '-y', default=False, action='store_true', help='Skips the sanity prompt.')

# Define required arguments
parsereq = parse.add_argument_group('required arguments')
parsereq.add_argument('--drive-id', '-d', help='The ID of the Shared Drive.', required=True)

# Parse arguments
args = parse.parse_args()

# Set variables from arguments
acc_dir = args.path  # Path to the service accounts folder
did = args.drive_id  # Drive ID for the shared drive
credentials = glob.glob(args.credentials)  # Credentials file path

# Check if credentials file exists
try:
    open(credentials[0], 'r')
    print('>> Found credentials.')
except IndexError:
    print('>> No credentials found.')
    sys.exit(0)

# Display sanity prompt if not skipped
if not args.yes:
    input('>> Make sure the **Google account** that has generated credentials.json\n   is added into your Team Drive '
          '(shared drive) as Manager\n>> (Press any key to continue)')

# Initialize credentials
creds = None

# Check if token_sa.pickle exists
if os.path.exists('token_sa.pickle'):
    # Load credentials from token_sa.pickle
    with open('token_sa.pickle', 'rb') as token:
        creds = pickle.load(token)

# If credentials are not valid, refresh or obtain new credentials
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        # Refresh credentials
        creds.refresh(Request())
    else:
        # Obtain new credentials
        flow = InstalledAppFlow.from_client_secrets_file(credentials[0], scopes=[
            'https://www.googleapis.com/auth/admin.directory.group',
            'https://www.googleapis.com/auth/admin.directory.group.member'
        ])
        creds = flow.run_console()  # run_local_server() for web application

    # Save credentials for the next run
    with open('token_sa.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Initialize Google Drive API client
drive = googleapiclient.discovery.build("drive", "v3", credentials=creds)

# Initialize batch request
batch = drive.new_batch_http_request()

# Read service accounts from the specified folder
aa = glob.glob('%s/*.json' % acc_dir)

# Initialize progress bar
pbar = progress.bar.Bar("Readying accounts", max=len(aa))

# Add permissions for each service account
for i in aa:
    ce = json.loads(open(i, 'r').read())['client_email']
    batch.add(drive.permissions().create(fileId=did, supportsAllDrives=True, body={
        "role": "organizer",
        "type": "user",
        "emailAddress": ce
    }))
    pbar.next()

# Finish progress bar
pbar.finish()

# Execute batch request
print('Adding...')
batch.execute()

# Display completion message
print('Complete.')

# Calculate elapsed time
hours, rem = divmod((time.time() - stt), 3600)
minutes, sec = divmod(rem, 60)
print("Elapsed Time:\n{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), sec))
