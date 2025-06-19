from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy with no app yet
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers_market.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize db with the app
    db.init_app(app)
    
    # Register blueprints
    from agrishield.routes import main
    app.register_blueprint(main)
    
    # Create the database if it doesn't exist
    with app.app_context():
        db.create_all()
        
        # Check if we need to load sample data
        from agrishield.models import Product
        if Product.query.count() == 0:
            from agrishield.sample_data import load_sample_data
            load_sample_data(db)
    
    return app
