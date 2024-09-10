import configparser
from googleapiclient.discovery import build
from google.oauth2 import service_account
from apiclient.http import MediaFileUpload

# Step 1: Read configuration from the config file
config = configparser.ConfigParser()
config.read('config.cfg')

# Retrieve the service account file path from the config
service_account_file = config['google']['creds']

# Step 2: Authentication and setup using the service account file from the config
creds = service_account.Credentials.from_service_account_file(
    service_account_file,
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=creds)

# Folder ID where the files will be uploaded
folder_id = '1u2EzmZj_V_wfg_5dY-z91E5hMTXRg_z_'

# Function to find and delete a file by name in a specific folder
def delete_existing_file(filename, folder_id):
    query = f"name = '{filename}' and '{folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if items:
        for item in items:
            drive_service.files().delete(fileId=item['id']).execute()
            print(f"Deleted existing file: {item['name']}")

# Helper function to upload a file
def upload_file(file_name, file_path, folder_id):
    # Set file metadata
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    # Create a media upload object
    media = MediaFileUpload(file_path, mimetype='text/csv')
    
    # Check and delete existing file if it exists
    delete_existing_file(file_name, folder_id)

    # Upload the new file
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded {file_name} with file ID: {file['id']}")

# Define the files to be uploaded
files_to_upload = [
    {'name': 'gender-sales.csv', 'path': '/Users/arunabhbora/Downloads/code/machine learning/data/gender_sales.csv'},
    {'name': 'member_sales.csv', 'path': '//Users/arunabhbora/Downloads/code/machine learning/data/member_sales.csv'},
    {'name': 'product line_sales.csv', 'path': '/Users/arunabhbora/Downloads/code/machine learning/data/productline_sales.csv'}
]

# Upload all files
for file in files_to_upload:
    upload_file(file['name'], file['path'], folder_id)
