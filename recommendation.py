from agrishield.models import Product, Review, Order, OrderItem
from flask import session
from sqlalchemy import func
import random

def get_recommendations(user_id):
    """Get product recommendations for a specific user"""
    # Get products the user has already ordered or reviewed
    user_products = set()
    
    # From orders
    ordered_items = OrderItem.query.join(Order).filter(Order.user_id == user_id).all()
    for item in ordered_items:
        user_products.add(item.product_id)
    
    # From reviews
    reviewed_products = Review.query.filter_by(user_id=user_id).all()
    for review in reviewed_products:
        user_products.add(review.product_id)
    
    # Get products in the same categories as what the user has already shown interest in
    categories = Product.query.filter(Product.id.in_(user_products)).with_entities(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    # If we have categories, recommend based on them
    if categories:
        recommended = Product.query.filter(
            Product.category.in_(categories),
            ~Product.id.in_(user_products)
        ).order_by(Product.rating.desc()).limit(6).all()
        
        # If we don't have enough, add some highly rated products
        if len(recommended) < 6:
            more_products = Product.query.filter(
                ~Product.id.in_(user_products),
                ~Product.id.in_([p.id for p in recommended])
            ).order_by(Product.rating.desc()).limit(6 - len(recommended)).all()
            
            recommended.extend(more_products)
            
        return recommended
    else:
        # If no categories, just get highly rated products
        return Product.query.order_by(Product.rating.desc()).limit(6).all()

def get_similar_products(product_id):
    """Get products similar to the specified product"""
    product = Product.query.get(product_id)
    if not product:
        return []
    
    # Get products in the same category
    similar_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product_id
    ).order_by(Product.rating.desc()).limit(4).all()
    
    # If we don't have enough, add some other highly rated products
    if len(similar_products) < 4:
        more_products = Product.query.filter(
            Product.id != product_id,
            ~Product.id.in_([p.id for p in similar_products])
        ).order_by(Product.rating.desc()).limit(4 - len(similar_products)).all()
        
        similar_products.extend(more_products)
    
    return similar_products