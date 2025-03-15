import os

db_path = os.path.join(os.getcwd(),'instance/api_developer.db')  # Update this with your actual database path

if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Database {db_path} deleted successfully.")
else:
    print(f"Database {db_path} not found.")