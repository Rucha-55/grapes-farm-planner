import os
import sys
import requests
from tqdm import tqdm
import re

def download_file_from_google_drive(file_id, destination):
    """
    Download a file from Google Drive using its file ID.
    Handles large file downloads and shows progress.
    """
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    
    # First request to get the download page
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    # Check if we got an HTML page (Google's warning page)
    content = response.text
    if '<!DOCTYPE html>' in content or '<html' in content.lower():
        # Extract the download confirmation token
        match = re.search(r'confirm=([0-9A-Za-z_]+)', content)
        if match:
            token = match.group(1)
            # Make a new request with the confirmation token
            response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)
        else:
            # If no token found, try to get the direct download link
            match = re.search(r'href=\"(/uc\\?export=download[^\"]+)', content)
            if match:
                download_url = 'https://drive.google.com' + match.group(1).replace('&amp;', '&')
                response = session.get(download_url, stream=True)
    
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
        
        # Verify the downloaded file is not an HTML error page
        if os.path.getsize(destination) < 1024:  # If file is too small, it's likely an error page
            with open(destination, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1024)
            if '<!DOCTYPE html>' in content or '<html' in content.lower() or 'Google Drive - Quota exceeded' in content:
                os.remove(destination)
                return False
        return True
            
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
    
    # Dictionary of model files and their Google Drive file IDs with minimum expected sizes (in bytes)
    model_files = {
        "grape_model.h5": {"id": "1xFJROCP69sNcH0E4TdD38OvSdIJUalGC", "min_size": 1000000},  # ~1MB
        "apple_disease.h5": {"id": "1HjIVeMdsnW40n3IMLUp1r68PmmVsrSFX", "min_size": 1000000},  # ~1MB
        "grape_leaf_disease_model.h5": {"id": "1dzGkGnDyC7yXKER1Q2X8z0ycDMWY1SQ3", "min_size": 1000000},  # ~1MB
        "scaler.pkl": {"id": "1cFdAGQAkYUjtLRpsRO8pyEfmZ9IPV9eY", "min_size": 100},  # At least 100 bytes
        "label_encoder.pkl": {"id": "14C9YCEts3Lza3iGHSnhrApN29JsqIJQU", "min_size": 100}  # At least 100 bytes
    }
    
    print("🔍 Checking for model files...")
    all_success = True
    
    for filename, file_info in model_files.items():
        file_id = file_info["id"]
        min_size = file_info["min_size"]
        file_path = os.path.join("models", filename)
        
        # Skip if file exists and meets minimum size requirement
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size >= min_size:
                file_size_mb = file_size / (1024 * 1024)
                print(f"✅ {filename} already exists ({file_size_mb:.2f} MB)")
                continue
            else:
                print(f"⚠️  {filename} exists but is too small ({file_size} bytes < {min_size} bytes), re-downloading...")
                os.remove(file_path)
        
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            print(f"\n⬇️  Downloading {filename} (attempt {attempt}/{max_retries})...")
            
            if download_file_from_google_drive(file_id, file_path):
                # Verify the downloaded file size
                if os.path.exists(file_path) and os.path.getsize(file_path) >= min_size:
                    file_size = os.path.getsize(file_path)
                    file_size_mb = file_size / (1024 * 1024)
                    print(f"✅ Successfully downloaded {filename} ({file_size_mb:.2f} MB)")
                    break
                else:
                    print(f"⚠️  Download completed but file size is too small, retrying...")
                    if os.path.exists(file_path):
                        os.remove(file_path)
            
            if attempt == max_retries:
                print(f"❌ Failed to download {filename} after {max_retries} attempts")
                all_success = False
                break
    
    # Final verification of all files
    print("\n🔍 Verifying all model files...")
    missing_files = []
    for filename, file_info in model_files.items():
        file_path = os.path.join("models", filename)
        if not os.path.exists(file_path) or os.path.getsize(file_path) < file_info["min_size"]:
            missing_files.append(filename)
    
    if not missing_files:
        print("🎉 All model files have been downloaded and verified successfully!")
        return True
    else:
        print(f"❌ Missing or incomplete files: {', '.join(missing_files)}")
        print("Please check the error messages above and try again.")
        return False

if __name__ == "__main__":
    success = download_models()
    sys.exit(0 if success else 1)
