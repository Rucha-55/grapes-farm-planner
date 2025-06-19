# Grape and Apple Disease Detection System

A machine learning-based web application for detecting diseases in grape and apple plants using deep learning models. This application helps farmers and agricultural experts quickly identify plant diseases and get recommendations for treatment.

## Features

- Detect diseases in grape leaves
- Detect diseases in apple leaves
- Get detailed information about detected diseases
- Receive treatment recommendations
- User-friendly web interface

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rucha-55/grapes-farm-planner.git
   cd grapes-farm-planner
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Activate the virtual environment** (if not already activated)
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the Flask application**
   ```bash
   python app.py
   ```

3. **Access the application**
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
.
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── uploads/              # Directory for uploaded images
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore file
```

## Models

This project uses the following pre-trained models:
- `grape_leaf_disease_model.h5` - For grape leaf disease detection
- `apple_disease.h5` - For apple leaf disease detection
- `grape_variety_model.pkl` - For grape variety classification

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Dataset credits: [PlantVillage Dataset](https://plantvillage.psu.edu/)
- Special thanks to all the open-source contributors whose work made this project possible.
