import requests
import random
from datetime import datetime, timedelta

# API endpoint
URL = "http://localhost:5001/orders"

# Sample product names
PRODUCTS = [
    "Laptop Dell XPS",
    "iPhone 15",
    "Samsung Galaxy S23",
    "MacBook Pro",
    "Sony PlayStation 5",
    "Xbox Series X",
    "Nintendo Switch",
    "iPad Air",
    'Smart TV Samsung 55"',
    "Wireless Headphones Bose",
    "GoPro Hero 11",
    "Mechanical Keyboard",
    "Gaming Mouse Logitech",
    "VR Headset Meta Quest 3",
    "Smartwatch Apple Watch Ultra",
    "DJI Mini 3 Drone",
    "Portable SSD 1TB",
    "Sony WH-1000XM5",
    'Monitor UltraWide 34"',
    "Amazon Echo Show",
]

# Generate 50 orders
for i in range(50):
    order_data = {
        "date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime(
            "%Y-%m-%d"
        ),
        "product": random.choice(PRODUCTS),  # Select a random product
    }

    response = requests.post(URL, json=order_data)
    print(f"Order {i+1}: Status {response.status_code}, Response: {response.json()}")
