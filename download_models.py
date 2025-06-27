import os
import sys
import urllib.request
import urllib.parse
import http.cookiejar
import re
import shutil
from tqdm import tqdm

def get_confirm_token(response):
    """Get the confirmation token from the cookies"""
    for key, value in response.getheaders():
        if key.startswith('Set-Cookie'):
            if 'download_warning' in value:
                match = re.search(r'download_warning=([^;]+)', value)
                if match:
                    return match.group(1)
    return None

def download_file(url, output_path):
    """
    Download a file from Google Drive with progress bar
    """
    try:
        # Create a cookie jar to handle cookies
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        urllib.request.install_opener(opener)
        
        # First request to get the confirmation token
        response = urllib.request.urlopen(url)
        token = get_confirm_token(response)
        
        if token:
            # If we got a token, we need to make another request to confirm
            url = f"{url}&confirm={token}"
            response = urllib.request.urlopen(url)
        
        # Get the total file size
        total_size = int(response.headers.get('content-length', 0))
        
        # Initialize progress bar
        block_size = 1024 * 8  # 8KB chunks
        progress_bar = tqdm(
            total=total_size, 
            unit='B', 
            unit_scale=True,
            desc=f"Downloading {os.path.basename(output_path)}"
        )
        
        # Download the file in chunks and update progress
        with open(output_path, 'wb') as f:
            while True:
                chunk = response.read(block_size)
                if not chunk:
                    break
                f.write(chunk)
                progress_bar.update(len(chunk))
        
        progress_bar.close()
        
        # Verify the file was downloaded correctly
        file_size = os.path.getsize(output_path)
        if file_size > 1024:  # Check if file is larger than 1KB (to avoid HTML error pages)
            print(f"Successfully downloaded {output_path} ({file_size/1024/1024:.2f} MB)")
            return True
        else:
            print(f"Downloaded file is too small (likely an error page): {output_path} ({file_size} bytes)")
            # Try to read the file to see if it's an HTML error page
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    if '<!DOCTYPE html>' in content or '<html' in content:
                        print("Error: Got an HTML error page instead of the model file")
                        print("This usually means the file is not publicly accessible or requires authentication")
            except:
                pass
            
            if os.path.exists(output_path):
                os.remove(output_path)
            return False
                
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return False

def download_models():
    """
    Download model files from Google Drive if they don't exist locally.
    """
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Dictionary of model files and their Google Drive file IDs
    model_files = {
        "models/grape_model.h5": "1xFJROCP69sNcH0E4TdD38OvSdIJUalGC",
        "models/apple_disease.h5": "1HjIVeMdsnW40n3IMLUp1r68PmmVsrSFX",
        "models/grape_leaf_disease_model.h5": "1dzGkGnDyC7yXKER1Q2X8z0ycDMWY1SQ3",
        "models/scaler.pkl": "1cFdAGQAkYUjtLRpsRO8pyEfmZ9IPV9eY",
        "models/label_encoder.pkl": "14C9YCEts3Lza3iGHSnhrApN29JsqIJQU"
    }
    
    # Expected minimum file sizes in bytes (to detect failed downloads)
    min_file_sizes = {
        "models/grape_model.h5": 100 * 1024 * 1024,  # ~100MB
        "models/apple_disease.h5": 100 * 1024 * 1024,  # ~100MB
        "models/grape_leaf_disease_model.h5": 100 * 1024 * 1024,  # ~100MB
        "models/scaler.pkl": 1 * 1024,  # ~1KB
        "models/label_encoder.pkl": 1 * 1024  # ~1KB
    }
    
    print("Checking for model files...")
    all_downloads_successful = True
    
    for file_path, file_id in model_files.items():
        # Skip if file exists and has sufficient size
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            min_size = min_file_sizes.get(file_path, 1024)  # Default to 1KB if not specified
            if file_size >= min_size:
                print(f"{file_path} already exists and is valid ({file_size/1024/1024:.2f} MB), skipping download")
                continue
            else:
                print(f"Existing file {file_path} is too small ({file_size} bytes), re-downloading...")
                os.remove(file_path)
        
        # Construct the download URL
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        print(f"\nDownloading {os.path.basename(file_path)} from Google Drive...")
        
        # Try to download the file
        success = download_file(url, file_path)
        
        if not success:
            print(f"Warning: Failed to download {file_path}")
            all_downloads_successful = False
            continue
            
        # Verify the downloaded file size
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            min_size = min_file_sizes.get(file_path, 1024)
            if file_size < min_size:
                print(f"Warning: Downloaded file {file_path} is too small ({file_size} bytes), may be corrupted")
                os.remove(file_path)
                all_downloads_successful = False
    
    if all_downloads_successful:
        print("\n✅ All model files have been downloaded successfully!")
    else:
        print("\n⚠️ Some files failed to download. Please check the error messages above.")
    
    return all_downloads_successful

if __name__ == "__main__":
    download_models()
