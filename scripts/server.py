from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path
import os

def google_download(folder_id, download_path):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile('credentials.json')
    
    if gauth.credentials is None:
        # Authenticate if they're not available
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh the credentials if expired
        gauth.Refresh()
    else:
        # Authorize with the credentials loaded from the saved file
        gauth.Authorize()

    # Save the credentials for the next run
    gauth.SaveCredentialsFile("credentials.json")

    drive = GoogleDrive(gauth)

    folder_query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': folder_query}).GetList()

    if not file_list:
        print("No files found in the folder.")
        return

    latest_file = max(file_list, key=lambda f: f['createdDate'])
    file_title = latest_file['title']
    file_id = latest_file['id']

    print(f"Downloading latest file: {file_title}")
    
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(os.path.join(download_path, 'health.json'))
    
    print("Download complete!")

if __name__ == "__main__":
    folder_id = "1nkJ6nzyznlUsoowAXmSe1bGbtz6UFst8"
    download_path = Path('data/')
    
    google_download(folder_id, download_path)
