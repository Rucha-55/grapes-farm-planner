from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from database import users_collection, products_collection, reviews_collection
from bson import ObjectId

def load_sample_data():
    """Add sample data to the database"""
    
    # Clear existing data
    users_collection.delete_many({})
    products_collection.delete_many({})
    reviews_collection.delete_many({})
    
    # Add sample users
    users = [
        {
            '_id': ObjectId(),
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'hashed_password_1',  # In production, use proper password hashing
            'created_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'password': 'hashed_password_2',  # In production, use proper password hashing
            'created_at': datetime.utcnow()
        }
    ]
    
    for user_data in users:
        users_collection.insert_one(user_data)
    
    # Add sample products
    products = [
        {
            '_id': ObjectId(),
            'name': 'GrapeShield Fungicide',
            'description': 'Effective fungicide specifically formulated to combat downy mildew, powdery mildew, and black rot in grape vineyards. Provides long-lasting protection for up to 14 days.',
            'price': 1299.99,
            'image': 'grapeshield.jpg',
            'category': 'pesticides',
            'stock': 25,
            'rating': 3,
            'review_count': 42,
            'usage': 'Mix 5ml per liter of water and spray evenly on grape vines every 7-14 days',
            'certification': 'Organic Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'VinePro Insecticide',
            'description': 'Specialized insecticide for controlling grape leafhoppers, thrips, and grape berry moths. Protects your vineyard from insect damage without affecting beneficial insects.',
            'price': 899.50,
            'image': 'vinepro.jpg',
            'category': 'pesticides',
            'stock': 18,
            'rating': 3,
            'review_count': 28,
            'usage': 'Apply 2-3ml per liter of water, spray during early morning or late evening',
            'certification': 'EPA Registered'
        },
        {
            '_id': ObjectId(),
            'name': 'AppleGuard Complete',
            'description': 'All-in-one solution for apple orchards, targeting apple scab, fire blight, and codling moth. This systemic pesticide provides both preventive and curative action.',
            'price': 1499.99,
            'image': 'appleguard.jpg',
            'category': 'pesticides',
            'stock': 15,
            'rating': 5,
            'review_count': 56,
            'usage': 'Apply 10ml per liter of water every 10-14 days during growing season',
            'certification': 'USDA Approved'
        },
        {
            '_id': ObjectId(),
            'name': 'OrchardShield Fungicide',
            'description': 'Specialized fungicide for apple orchards, effective against apple scab, powdery mildew, and cedar apple rust. Rainfast within 1 hour of application.',
            'price': 1199.00,
            'image': 'orchardshield.jpg',
            'category': 'pesticides',
            'stock': 22,
            'rating': 2,
            'review_count': 34,
            'usage': 'Mix 7ml per liter of water and apply as a foliar spray',
            'certification': 'EPA Registered'
        },
        {
            '_id': ObjectId(),
            'name': 'ApplePro Insect Control',
            'description': 'Targeted insecticide for apple maggot, codling moth, and apple aphids. Provides up to 21 days of protection with a single application.',
            'price': 999.50,
            'image': 'appleproinsect.jpg',
            'category': 'pesticides',
            'stock': 20,
            'rating': 4,
            'review_count': 31,
            'usage': 'Apply 5ml per liter of water, best used at first sign of infestation',
            'certification': 'OMRI Listed'
        },
        {
            '_id': ObjectId(),
            'name': 'Grape Seedlings - Cabernet Sauvignon',
            'description': 'Premium Cabernet Sauvignon grape vine seedlings, grafted onto phylloxera-resistant rootstock. These hardy vines produce excellent wine grapes with rich flavor profiles.',
            'price': 499.99,
            'image': 'grapesampling.jpg',
            'category': 'seedlings',
            'stock': 30,
            'rating': 5,
            'review_count': 48,
            'usage': 'Plant in well-drained soil with full sun exposure',
            'certification': 'Virus-Free Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Apple Tree Sapling - Honeycrisp',
            'description': 'Honeycrisp apple tree saplings, known for producing sweet, crisp apples with excellent storage quality. These 2-year-old saplings will begin fruiting within 2-3 years.',
            'price': 799.00,
            'image': 'appletreesapling.jpg',
            'category': 'seedlings',
            'stock': 25,
            'rating': 3,
            'review_count': 52,
            'usage': 'Requires cross-pollination with another apple variety',
            'certification': 'Disease-Free Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Grape Seedlings - Thompson Seedless',
            'description': 'Thompson Seedless grape vine seedlings, perfect for table grapes or raisins. These vigorous vines are adaptable to various soil conditions and produce high yields.',
            'price': 449.99,
            'image': 'grapethomsan.jpg',
            'category': 'seedlings',
            'stock': 28,
            'rating': 3,
            'review_count': 37,
            'usage': 'Plant 8-10 feet apart in rows',
            'certification': 'Virus-Free Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Apple Tree Sapling - Granny Smith',
            'description': 'Granny Smith apple tree saplings, producing tart green apples perfect for baking and fresh eating. These saplings are grafted onto semi-dwarf rootstock for easier management.',
            'price': 749.00,
            'image': 'applegraney.jpg',
            'category': 'seedlings',
            'stock': 22,
            'rating': 4,
            'review_count': 41,
            'usage': 'Requires 600-800 chill hours',
            'certification': 'Disease-Free Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Organic Compost - Vineyard Blend',
            'description': 'Specially formulated organic compost for vineyards, enriched with mycorrhizal fungi and beneficial bacteria. Improves soil structure and provides slow-release nutrients.',
            'price': 599.99,
            'image': 'vineyard_compost.jpg',
            'category': 'organic',
            'stock': 40,
            'rating': 3,
            'review_count': 45,
            'usage': 'Apply 2-3kg per vine annually',
            'certification': 'OMRI Listed, Organic Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Organic Orchard Fertilizer',
            'description': 'Balanced organic fertilizer specifically designed for fruit trees. Contains essential macro and micronutrients for healthy growth and abundant fruit production.',
            'price': 649.50,
            'image': 'orchard_fertilizer.jpg',
            'category': 'organic',
            'stock': 35,
            'rating': 3,
            'review_count': 39,
            'usage': 'Apply 1kg per tree in early spring and mid-summer',
            'certification': 'OMRI Listed, USDA Organic'
        },
        {
            '_id': ObjectId(),
            'name': 'Organic Pest Repellent - Neem Oil',
            'description': 'Pure neem oil extract, an effective organic solution for controlling a wide range of pests and fungal diseases in vineyards and orchards without harming beneficial insects.',
            'price': 399.99,
            'image': 'neem_oil.jpg',
            'category': 'organic',
            'stock': 45,
            'rating': 5,
            'review_count': 33,
            'usage': 'Mix 5ml with 1 liter of water and a drop of mild soap',
            'certification': 'OMRI Listed, Organic Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Organic Soil Conditioner',
            'description': 'Premium organic soil conditioner with humic acids and seaweed extract. Improves soil structure, water retention, and nutrient availability for healthier plants.',
            'price': 549.00,
            'image': 'soil_conditioner.jpg',
            'category': 'organic',
            'stock': 38,
            'rating': 2,
            'review_count': 29,
            'usage': 'Mix 5kg per 100 square meters of soil',
            'certification': 'OMRI Listed, USDA Organic'
        },
        {
            '_id': ObjectId(),
            'name': 'Organic Weed Control Fabric',
            'description': 'Biodegradable weed control fabric made from organic materials. Suppresses weeds while allowing water and nutrients to reach plant roots. Ideal for vineyards and orchards.',
            'price': 899.99,
            'image': 'weed_fabric.jpg',
            'category': 'organic',
            'stock': 30,
            'rating': 4,
            'review_count': 27,
            'usage': 'Lay around plants with edges secured by soil or stakes',
            'certification': 'Biodegradable Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Organic Grape Disease Control',
            'description': 'OMRI-listed organic fungicide specifically formulated for grape diseases. Contains potassium bicarbonate and botanical extracts to control powdery mildew and other fungal issues.',
            'price': 799.50,
            'image': 'organic_grape_control.jpg',
            'category': 'organic',
            'stock': 25,
            'rating': 3,
            'review_count': 36,
            'usage': 'Apply weekly during high disease pressure periods',
            'certification': 'OMRI Listed, Organic Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'BlackRot Defender',
            'description': 'Fungicide containing captan, effective against black rot in grape vineyards. Promotes healthy vine growth and reduces disease spread.',
            'price': 999.99,
            'image': 'blackrot_defender.jpg',
            'category': 'pesticides',
            'stock': 20,
            'rating': 3,
            'review_count': 38,
            'usage': 'Apply 4-5ml per liter of water, spray every 10-14 days during growing season',
            'certification': 'EPA Registered'
        },
        {
            '_id': ObjectId(),
            'name': 'LeafBlight Guard',
            'description': 'Copper-based fungicide for preventing leaf blight in grape vineyards. Enhances vine health and prevents fungal infections.',
            'price': 799.50,
            'image': 'leafblight_guard.jpg',
            'category': 'pesticides',
            'stock': 18,
            'rating': 3,
            'review_count': 32,
            'usage': 'Mix 3ml per liter of water, apply as a foliar spray every 7-10 days',
            'certification': 'EPA Registered'
        },
        {
            '_id': ObjectId(),
            'name': 'ESCA Shield',
            'description': 'Fungicide with sulfur and potassium bicarbonate, specifically formulated to combat ESCA in grape vineyards. Improves vine health and reduces disease incidence.',
            'price': 1099.00,
            'image': 'esca_shield.jpg',
            'category': 'pesticides',
            'stock': 22,
            'rating': 3,
            'review_count': 40,
            'usage': 'Apply 6ml per liter of water, spray every 14 days during high disease pressure',
            'certification': 'EPA Registered'
        },
        {
            '_id': ObjectId(),
            'name': 'Vineyard Health Kit',
            'description': 'Comprehensive kit for maintaining healthy grape vineyards. Includes tools for regular monitoring, balanced fertilization, and proper pruning practices.',
            'price': 1499.99,
            'image': 'vineyard_health_kit.jpg',
            'category': 'tools',
            'stock': 30,
            'rating': 5,
            'review_count': 50,
            'usage': 'Follow included instructions for regular vineyard maintenance',
            'certification': 'Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'HealthyVine Fertilizer',
            'description': 'Balanced organic fertilizer designed for maintaining healthy grape vines. Provides essential nutrients for robust growth and disease resistance.',
            'price': 699.50,
            'image': 'healthyvine_fertilizer.jpg',
            'category': 'organic',
            'stock': 35,
            'rating': 3,
            'review_count': 42,
            'usage': 'Apply 1.5kg per vine in early spring and mid-summer',
            'certification': 'OMRI Listed, USDA Organic'
        },
        {
            '_id': ObjectId(),
            'name': 'Pruning Shears Pro',
            'description': 'High-quality pruning shears for maintaining proper air circulation in grape vineyards. Essential for disease prevention and healthy vine growth.',
            'price': 299.99,
            'image': 'pruning_shears_pro.jpg',
            'category': 'tools',
            'stock': 50,
            'rating': 5,
            'review_count': 55,
            'usage': 'Use for precise pruning of grape vines',
            'certification': 'Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Irrigation System Kit',
            'description': 'Advanced irrigation system kit to avoid overhead watering and reduce disease spread in vineyards. Includes drip irrigation components for efficient water delivery.',
            'price': 1999.00,
            'image': 'irrigation_system_kit.jpg',
            'category': 'tools',
            'stock': 25,
            'rating': 4,
            'review_count': 58,
            'usage': 'Install according to included instructions for optimal vineyard irrigation',
            'certification': 'Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Grape Vine Tying Kit',
            'description': 'Kit containing biodegradable ties and stakes for training grape vines. Ensures proper vine support and growth.',
            'price': 149.99,
            'image': 'grape_vine_tying_kit.jpg',
            'category': 'tools',
            'stock': 50,
            'rating': 5,
            'review_count': 55,
            'usage': 'Use ties to secure grape vines to stakes or trellis',
            'certification': 'Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Grape Canopy Management Tool',
            'description': 'Tool for managing grape canopy density. Helps in improving sunlight penetration and reducing disease risk.',
            'price': 299.99,
            'image': 'grape_canopy_management_tool.jpg',
            'category': 'tools',
            'stock': 45,
            'rating': 4,
            'review_count': 50,
            'usage': 'Use to thin out excess foliage for better vine health',
            'certification': 'Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Grape Vine Grafting Kit',
            'description': 'Complete grafting kit for propagating grape vines. Includes grafting tools, tape, and instructions for successful grafting.',
            'price': 199.99,
            'image': 'grape_vine_grafting_kit.jpg',
            'category': 'tools',
            'stock': 40,
            'rating': 5,
            'review_count': 48,
            'usage': 'Follow included instructions for grafting grape vines',
            'certification': 'Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Grape Vine Support Netting',
            'description': 'Heavy-duty netting for supporting grape vines. Provides additional support and helps in maintaining vine structure.',
            'price': 399.99,
            'image': 'grape_vine_support_netting.jpg',
            'category': 'tools',
            'stock': 35,
            'rating': 4,
            'review_count': 45,
            'usage': 'Install netting around grape vines for support',
            'certification': 'Certified'
        },
        {
            '_id': ObjectId(),
            'name': 'Grape Harvesting Basket',
            'description': 'Ergonomic basket for grape harvesting. Designed to hold grapes securely and reduce damage during collection.',
            'price': 79.99,
            'image': 'grape_harvesting_basket.jpg',
            'category': 'tools',
            'stock': 60,
            'rating': 4,
            'review_count': 55,
            'usage': 'Use basket to collect grapes during harvest',
            'certification': 'Certified'
        }
    ]
    
    for product_data in products:
        products_collection.insert_one(product_data)
    
    # Add sample reviews
    reviews = [
        {
            '_id': ObjectId(),
            'product_id': products[0]['_id'],
            'user_id': users[0]['_id'],
            'rating': 5,
            'comment': 'These products are amazing! So effective and reliable.',
            'created_at': datetime.utcnow() - timedelta(days=5)
        },
        {
            '_id': ObjectId(),
            'product_id': products[1]['_id'],
            'user_id': users[1]['_id'],
            'rating': 4,
            'comment': 'Great quality products, I love supporting local farmers.',
            'created_at': datetime.utcnow() - timedelta(days=10)
        },
        {
            '_id': ObjectId(),
            'product_id': products[2]['_id'],
            'user_id': users[0]['_id'],
            'rating': 4,
            'comment': 'The tools are durable and well-made.',
            'created_at': datetime.utcnow() - timedelta(days=2)
        }
    ]
    
    for review_data in reviews:
        reviews_collection.insert_one(review_data)
    
    print('Sample data loaded successfully!')