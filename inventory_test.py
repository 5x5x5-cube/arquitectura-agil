import requests

# API endpoint for Inventory Service
URL = "http://localhost:5002/products"

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

# Add each product to the inventory (only once)
for i, product in enumerate(PRODUCTS, start=1):
    product_data = {"name": product}

    response = requests.post(URL, json=product_data)

    # Print result
    if response.status_code == 201:
        print(f"✅ Product {i}: {product} added successfully!")
    elif response.status_code == 400:
        print(f"⚠️ Product {i}: {product} already exists.")
    else:
        print(
            f"❌ Product {i}: Failed to add ({response.status_code}). Response: {response.text}"
        )
