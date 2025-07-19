# Grape and Apple Disease Detection System

A machine learning-based web application for detecting diseases in grape and apple plants using deep learning models. This application helps farmers and agricultural experts quickly identify plant diseases and get recommendations for treatment.

## Features

- Detect diseases in grape leaves
- Detect diseases in apple leaves
- Get detailed information about detected diseases
- Receive treatment recommendations
- User-friendly web interface
- Responsive design for mobile and desktop
- Secure user authentication
- Farm management dashboard
- Weather integration
- PDF report generation

## Prerequisites

- Python 3.9.18
- pip (Python package manager)
- Git (for cloning the repository)
- MongoDB Atlas account (for production database)
- OpenWeatherMap API key (for weather data)
- Google Gemini API key (for AI recommendations)
- Render account (for deployment)

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: MongoDB
- **Machine Learning**: TensorFlow, Keras
- **Deployment**: Docker, Gunicorn, Render
- **CI/CD**: GitHub Actions (optional)

## Local Development

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rucha-55/grapes-farm-planner.git
   cd grapes-farm-planner
   ```

2. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the environment variables with your configuration

3. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database**
   - Make sure MongoDB is running locally or update the `MONGO_URI` in `.env`
   - The application will create the necessary collections on first run

### Running the Application

1. **Development mode**
   ```bash
   flask run --debug
   ```
   The application will be available at `http://localhost:5000`

2. **Production mode**
   ```bash
   gunicorn --config gunicorn_config.py app:app
   ```
   The application will be available at `http://localhost:10000`

## Deployment

### Prerequisites

- GitHub account
- Render.com account
- MongoDB Atlas cluster
- OpenWeatherMap API key
- Google Gemini API key

### Deploying to Render

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service** on Render:
   - Click the "New +" button and select "Web Service"
   - Connect your GitHub account and select the forked repository
   - Configure the deployment:
     - **Name**: grapes-farm-planner (or your preferred name)
     - **Region**: Choose the region closest to your users
     - **Branch**: main (or your preferred branch)
     - **Build Command**: `./render-build.sh`
     - **Start Command**: `gunicorn --config gunicorn_config.py app:app`
     - **Plan**: Start with Free, upgrade as needed

3. **Set up environment variables** in the Render dashboard:
   - `FLASK_APP`: `app.py`
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generate a secure random string
   - `MONGO_URI`: Your MongoDB Atlas connection string
   - `WEATHER_API_KEY`: Your OpenWeatherMap API key
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `TF_CPP_MIN_LOG_LEVEL`: `3` (to reduce TensorFlow logs)
   - `TF_ENABLE_ONEDNN_OPTS`: `0`
   - `UPLOAD_FOLDER`: `/app/uploads`
   - `MAX_CONTENT_LENGTH`: `16777216` (16MB)

4. **Deploy** the application
   - Click "Create Web Service" to start the deployment
   - The build process might take several minutes as it installs all dependencies

5. **Access your application**
   - Once deployed, your app will be available at `https://<your-app-name>.onrender.com`

### File Storage Note

By default, uploaded files are stored in the container's filesystem, which is ephemeral. For production use:

1. **Option 1**: Use Render's disk storage (persistent but limited to free tier)
   - Uncomment the `volumes` section in `render.yaml`
   - Allocate appropriate storage size

2. **Option 2**: Use a cloud storage service (recommended for production)
   - Configure AWS S3, Google Cloud Storage, or similar
   - Update the file upload logic to use the cloud storage

### Monitoring and Maintenance

- Check the logs in the Render dashboard for any issues
- Set up monitoring and alerts in the Render dashboard
- Consider upgrading to a paid plan for production use

### Using Docker (Optional)

1. **Build the Docker image**
   ```bash
   docker build -t grapes-farm-planner .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 10000:10000 --env-file .env grapes-farm-planner
   ```

## Environment Variables

See `.env.example` for a list of required environment variables.

## API Documentation

The application provides the following API endpoints:

- `GET /health` - Health check endpoint
- `POST /api/predict` - Image prediction endpoint
- `GET /api/weather` - Weather data endpoint

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [TensorFlow](https://www.tensorflow.org/)
- [Flask](https://flask.palletsprojects.com/)
- [MongoDB](https://www.mongodb.com/)
- [Bootstrap](https://getbootstrap.com/)
- [OpenWeatherMap](https://openweathermap.org/)
- [Google Gemini](https://ai.google/)

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
