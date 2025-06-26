import os
import sys
import gdown
import urllib.request
import shutil

def download_with_retry(url, output, max_retries=3):
    """Download a file with retry logic."""
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries} - Downloading {url}...")
            gdown.download(url, output, quiet=False)
            if os.path.exists(output) and os.path.getsize(output) > 0:
                print(f"Successfully downloaded {output}")
                return True
            else:
                print(f"Downloaded file is empty or doesn't exist: {output}")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if os.path.exists(output):
                os.remove(output)
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
    
    print("Checking for model files...")
    
    for file_path, file_id in model_files.items():
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            print(f"Need to download {file_path}...")
            url = f"https://drive.google.com/uc?id={file_id}"
            success = download_with_retry(url, file_path)
            if not success:
                print(f"Failed to download {file_path} after multiple attempts")
                # Try alternative download method
                try:
                    print("Trying alternative download method...")
                    url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    with urllib.request.urlopen(url) as response, open(file_path, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                    print(f"Successfully downloaded {file_path} using alternative method")
                except Exception as e:
                    print(f"Error downloading {file_path} using alternative method: {str(e)}")
        else:
            print(f"{file_path} already exists and is valid, skipping download")

if __name__ == "__main__":
    download_models()
