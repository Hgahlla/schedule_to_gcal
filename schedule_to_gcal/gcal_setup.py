import os
from shutil import copyfile
import subprocess
import datetime
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Creates the Google Calendar Service
def create_service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    token_path = "token.json"

    # Checks if the script is running on AWS Lambda
    if os.name != 'nt':
        # Set working dir to /tmp as lambda only has access to that
        tmp_dir = os.path.join(os.path.sep, "tmp", "schedule-to-gcal")
        token_path = os.path.join(tmp_dir, 'token.json')
        try:
            os.makedirs(tmp_dir)
            subprocess.run(["chmod", "775", str(tmp_dir)])
            copyfile('token.json', token_path)
            print("Created Directory & Copied File")
        except:
            pass
        os.chdir(tmp_dir)

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        # Google Calendar Service is Created Successfully
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        return service
    except Exception as e:
        print(e)
        return None


def convert_to_rfc_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


def convert_str_to_datetime(date):
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    local_tz = pytz.timezone('America/Chicago')
    local_dt = local_tz.localize(dt)
    return local_dt


def convert_to_utc(dt):
    utc = pytz.timezone('UTC')
    utc_dt = dt.astimezone(utc)
    return utc_dt


def add_time(hr=0, min=0):
    time = datetime.timedelta(hours=hr, minutes=min)
    return time
