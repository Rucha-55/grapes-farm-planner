import os
import gdown

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
        if not os.path.exists(file_path):
            print(f"Downloading {file_path}...")
            url = f"https://drive.google.com/uc?id={file_id}"
            try:
                gdown.download(url, file_path, quiet=False)
                print(f"Successfully downloaded {file_path}")
            except Exception as e:
                print(f"Error downloading {file_path}: {str(e)}")
        else:
            print(f"{file_path} already exists, skipping download")

if __name__ == "__main__":
    download_models()
