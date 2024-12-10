import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000/items"

USERNAME = "admin"
PASSWORD = "password"

def get_items():
    # Fetch all items
    response = requests.get(BASE_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Items in catalog:")
        for item in response.json()['data']:
            print(item)
    else:
        print(f"Error: {response.status_code}, {response.text}")

def add_item():
    # Add a new item
    name = input("Enter item name: ")
    price = float(input("Enter item price: "))
    quantity = int(input("Enter item quantity: "))
    warehouse = input("Enter warehouse (optional): ")
    payload = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "warehouse": warehouse
    }
    response = requests.post(BASE_URL, json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 201:
        print("Item added successfully:", response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")

def update_item():
    # Update an existing item
    item_id = int(input("Enter item ID to update: "))
    print("Leave fields blank to keep them unchanged.")
    name = input("Enter new name: ")
    price = input("Enter new price: ")
    quantity = input("Enter new quantity: ")
    warehouse = input("Enter new warehouse: ")

    payload = {}
    if name:
        payload["name"] = name
    if price:
        payload["price"] = float(price)
    if quantity:
        payload["quantity"] = int(quantity)
    if warehouse:
        payload["warehouse"] = warehouse

    response = requests.put(f"{BASE_URL}/{item_id}", json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Item updated successfully:", response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")

def delete_item():
    # Delete an item by ID
    item_id = int(input("Enter item ID to delete: "))
    response = requests.delete(f"{BASE_URL}/{item_id}", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Item deleted successfully.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def main():
    # Interactive menu
    while True:
        print("\n--- Menu ---")
        print("1. Get all items")
        print("2. Add item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            get_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
