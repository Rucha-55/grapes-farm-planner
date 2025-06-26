import os
import sys
import urllib.request
import shutil
from tqdm import tqdm

def download_file(url, output_path):
    """
    Download a file from a URL with progress bar
    """
    try:
        # Open the URL
        with urllib.request.urlopen(url) as response:
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
            if os.path.getsize(output_path) > 0:
                print(f"Successfully downloaded {output_path}")
                return True
            else:
                print(f"Downloaded file is empty: {output_path}")
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
    
    # Dictionary of model files and their direct download URLs
    model_files = {
        "models/grape_model.h5": "https://drive.google.com/uc?export=download&id=1xFJROCP69sNcH0E4TdD38OvSdIJUalGC",
        "models/apple_disease.h5": "https://drive.google.com/uc?export=download&id=1HjIVeMdsnW40n3IMLUp1r68PmmVsrSFX",
        "models/grape_leaf_disease_model.h5": "https://drive.google.com/uc?export=download&id=1dzGkGnDyC7yXKER1Q2X8z0ycDMWY1SQ3",
        "models/scaler.pkl": "https://drive.google.com/uc?export=download&id=1cFdAGQAkYUjtLRpsRO8pyEfmZ9IPV9eY",
        "models/label_encoder.pkl": "https://drive.google.com/uc?export=download&id=14C9YCEts3Lza3iGHSnhrApN29JsqIJQU"
    }
    
    print("Checking for model files...")
    
    for file_path, url in model_files.items():
        # Skip if file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"{file_path} already exists and is valid, skipping download")
            continue
            
        print(f"\nDownloading {os.path.basename(file_path)}...")
        
        # Try direct download first
        if not download_file(url, file_path):
            # If direct download fails, try alternative URL format
            print(f"Direct download failed, trying alternative URL...")
            file_id = url.split('id=')[1]
            alt_url = f"https://drive.google.com/uc?export=download&confirm=t&id={file_id}"
            if not download_file(alt_url, file_path):
                print(f"Failed to download {file_path} after multiple attempts")
                return False
    
    print("\nAll model files have been downloaded successfully!")
    return True

if __name__ == "__main__":
    download_models()
