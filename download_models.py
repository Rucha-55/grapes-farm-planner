import os
import sys
import requests
from tqdm import tqdm

def download_file_from_google_drive(file_id, destination):
    """
    Download a file from Google Drive using its file ID.
    Handles large file downloads and shows progress.
    """
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    
    # Initial request to get the download URL
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    # Get the confirmation token if it exists
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break
    
    # If we got a token, make another request with it
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    # Get the file size for the progress bar
    total_size = int(response.headers.get('content-length', 0))
    
    # Create parent directory if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Download the file in chunks and show progress
    chunk_size = 32768  # 32KB chunks
    
    try:
        with open(destination, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Downloading {os.path.basename(destination)}",
            ) as pbar:
                for chunk in response.iter_content(chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        # Verify the file was downloaded correctly
        if os.path.getsize(destination) > 1024:  # At least 1KB
            file_size_mb = os.path.getsize(destination) / (1024 * 1024)
            print(f"✅ Successfully downloaded {os.path.basename(destination)} ({file_size_mb:.2f} MB)")
            return True
        else:
            print(f"❌ Downloaded file is too small: {os.path.basename(destination)}")
            if os.path.exists(destination):
                os.remove(destination)
            return False
            
    except Exception as e:
        print(f"❌ Error downloading {os.path.basename(destination)}: {str(e)}")
        if os.path.exists(destination):
            os.remove(destination)
        return False

def download_models():
    """
    Download all required model files from Google Drive.
    """
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Dictionary of model files and their Google Drive file IDs
    model_files = {
        "grape_model.h5": "1xFJROCP69sNcH0E4TdD38OvSdIJUalGC",
        "apple_disease.h5": "1HjIVeMdsnW40n3IMLUp1r68PmmVsrSFX",
        "grape_leaf_disease_model.h5": "1dzGkGnDyC7yXKER1Q2X8z0ycDMWY1SQ3",
        "scaler.pkl": "1cFdAGQAkYUjtLRpsRO8pyEfmZ9IPV9eY",
        "label_encoder.pkl": "14C9YCEts3Lza3iGHSnhrApN29JsqIJQU"
    }
    
    print("🔍 Checking for model files...")
    all_success = True
    
    for filename, file_id in model_files.items():
        file_path = os.path.join("models", filename)
        
        # Skip if file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 1024:  # At least 1KB
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"✅ {filename} already exists ({file_size_mb:.2f} MB)")
            continue
            
        print(f"\n⬇️  Downloading {filename}...")
        
        if not download_file_from_google_drive(file_id, file_path):
            print(f"❌ Failed to download {filename}")
            all_success = False
            continue
            
    if all_success:
        print("\n🎉 All model files have been downloaded successfully!")
    else:
        print("\n❌ Some files failed to download. Please check the error messages above.")
    
    return all_success

if __name__ == "__main__":
    success = download_models()
    sys.exit(0 if success else 1)
