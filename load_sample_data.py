from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# MongoDB connection settings
MONGO_URI = "mongodb://root:example@localhost:27017/"

# Sample product data
products = [
    {"name": "Laptop", "price": 999.99},
    {"name": "Smartphone", "price": 699.99},
    {"name": "Headphones", "price": 199.99},
    {"name": "Tablet", "price": 499.99},
    {"name": "Smartwatch", "price": 299.99}
]

# Sample customer data
customers = [
    {"id": "C001", "name": "John Doe", "email": "john@example.com"},
    {"id": "C002", "name": "Jane Smith", "email": "jane@example.com"},
    {"id": "C003", "name": "Bob Johnson", "email": "bob@example.com"},
    {"id": "C004", "name": "Alice Brown", "email": "alice@example.com"},
    {"id": "C005", "name": "Charlie Wilson", "email": "charlie@example.com"}
]

def generate_order():
    order_date = datetime.now() - timedelta(days=random.randint(0, 30))
    product = random.choice(products)
    customer = random.choice(customers)
    quantity = random.randint(1, 5)
    
    return {
        "order_id": f"ORD-{random.randint(1000, 9999)}",
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "customer_email": customer["email"],
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "total_amount": round(quantity * product["price"], 2),
        "order_date": order_date,
        "status": random.choice(["pending", "shipped", "delivered"])
    }

def main():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client.sample_db
    orders_collection = db.orders

    # Clear existing orders
    orders_collection.delete_many({})

    # Generate and insert sample orders
    sample_orders = [generate_order() for _ in range(20)]
    orders_collection.insert_many(sample_orders)

    print(f"Successfully inserted {len(sample_orders)} sample orders into MongoDB")
    
    # Print a sample order
    print("\nSample order:")
    print(orders_collection.find_one())

if __name__ == "__main__":
    main() 