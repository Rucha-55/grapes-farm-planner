from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import os

# MongoDB connection string
MONGO_URI = 'mongodb+srv://smshelke:smshelke370122@cluster0.l2jnk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

try:
    # Create MongoDB client
    client = MongoClient(MONGO_URI)
    
    # Test the connection
    client.server_info()
    
    # Get database
    db = client.agrishield
    
    # Collections
    users_collection = db.users
    products_collection = db.products
    reviews_collection = db.reviews
    orders_collection = db.orders
    
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

def init_db():
    """Initialize database with required indexes"""
    try:
        # Create indexes
        users_collection.create_index('email', unique=True)
        products_collection.create_index('category')
        reviews_collection.create_index('product_id')
        reviews_collection.create_index('user_id')
        orders_collection.create_index('user_id')
        orders_collection.create_index('status')
        print("Database indexes created successfully!")
    except Exception as e:
        print(f"Error creating indexes: {e}")
        raise

def get_user_by_email1(email):
    """Get user by email"""
    try:
        return users_collection.find_one({'email': email})
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_product_by_id(product_id):
    """Get product by ID"""
    try:
        return products_collection.find_one({'_id': ObjectId(product_id)})
    except Exception as e:
        print(f"Error getting product: {e}")
        return None

def get_reviews_by_product(product_id):
    """Get all reviews for a product"""
    try:
        return list(reviews_collection.find({'product_id': ObjectId(product_id)}))
    except Exception as e:
        print(f"Error getting reviews: {e}")
        return []

def get_orders_by_user(user_id):
    """Get all orders for a user"""
    try:
        return list(orders_collection.find({'user_id': ObjectId(user_id)}))
    except Exception as e:
        print(f"Error getting orders: {e}")
        return []

def update_product_rating(product_id):
    """Update product rating based on reviews"""
    try:
        # Get all reviews for the product
        reviews = list(reviews_collection.find({'product_id': ObjectId(product_id)}))
        
        if not reviews:
            return
        
        # Calculate average rating
        total_rating = sum(review['rating'] for review in reviews)
        average_rating = total_rating / len(reviews)
        
        # Update product
        products_collection.update_one(
            {'_id': ObjectId(product_id)},
            {
                '$set': {
                    'rating': average_rating,
                    'review_count': len(reviews)
                }
            }
        )
    except Exception as e:
        print(f"Error updating product rating: {e}")
        raise 