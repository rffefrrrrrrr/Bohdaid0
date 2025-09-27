import json
import os
from pymongo import MongoClient
from datetime import datetime
import sys

def import_collection_to_mongodb(client, database_name, collection_name, json_file_path):
    """
    Import JSON data to a MongoDB collection
    """
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print(f"No data to import for collection {collection_name}")
            return 0
        
                # Clear existing data (uncommented to prevent duplicate key errors)
        collection.delete_many({})
        
        # Insert the data
        if len(data) == 1:
            result = collection.insert_one(data[0])
            inserted_count = 1 if result.inserted_id else 0
        else:
            result = collection.insert_many(data)
            inserted_count = len(result.inserted_ids)
        
        print(f"Successfully imported {inserted_count} documents to {collection_name}")
        return inserted_count
        
    except Exception as e:
        print(f"Error importing {collection_name}: {e}")
        return 0

def main():
    # MongoDB connection details
    mongodb_uri = os.getenv('MONGODB_URI')
    database_name = os.getenv('MONGODB_DATABASE', 'telegram_bot')
    
    if not mongodb_uri:
        print("Error: MONGODB_URI environment variable not set")
        print("Please set it to your MongoDB Atlas connection string:")
        print("export MONGODB_URI='mongodb+srv://username:password@cluster.mongodb.net/'")
        sys.exit(1)
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        # Test connection
        client.admin.command('ping')
        print(f"Connected to MongoDB successfully")
        print(f"Database: {database_name}")
        
        # Directory containing the transformed JSON files
        data_dir = "Aloobohdaid/transformed_mongodb_data"
        
        # Collections to import (in order of dependencies)
        collections = [
            "users",
            "responses", 
            "subscriptions",
            "sessions",
            "groups",
            "posts",
            "messages",
            "active_tasks",
            "status_updates",
            "scheduled_posts",
            "post_groups",
            "referrals",
            "settings"
        ]
        
        total_imported = 0
        
        for collection_name in collections:
            json_file = os.path.join(data_dir, f"{collection_name}.json")
            
            if os.path.exists(json_file):
                imported_count = import_collection_to_mongodb(
                    client, database_name, collection_name, json_file
                )
                total_imported += imported_count
            else:
                print(f"JSON file not found for {collection_name}: {json_file}")
        
        print(f"\nImport completed. Total documents imported: {total_imported}")
        
        # Verify the import by counting documents in each collection
        print("\nVerification - Document counts per collection:")
        db = client[database_name]
        for collection_name in collections:
            count = db[collection_name].count_documents({})
            print(f"{collection_name}: {count} documents")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()
