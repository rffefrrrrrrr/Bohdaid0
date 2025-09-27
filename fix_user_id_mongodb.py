import os
from pymongo import MongoClient
import sys

def fix_user_id_field():
    """
    Fix the user_id field issue in MongoDB by adding user_id field to all documents
    where it's missing, using the _id value.
    """
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
        
        db = client[database_name]
        
        # Collections that need user_id field added/fixed
        collections_to_fix = {
            'users': {'id_field': '_id', 'target_field': 'user_id'},
            'responses': {'id_field': '_id', 'target_field': 'id'},
            'subscriptions': {'id_field': '_id', 'target_field': 'id'},
            'groups': {'id_field': '_id', 'target_field': 'id'},
            'posts': {'id_field': '_id', 'target_field': 'id'},
            'messages': {'id_field': '_id', 'target_field': 'id'},
            'status_updates': {'id_field': '_id', 'target_field': 'id'},
        }
        
        total_updated = 0
        
        for collection_name, config in collections_to_fix.items():
            collection = db[collection_name]
            id_field = config['id_field']
            target_field = config['target_field']
            
            print(f"\nProcessing collection: {collection_name}")
            
            # Find documents that don't have the target field or where it's None
            query = {
                "$or": [
                    {target_field: {"$exists": False}},
                    {target_field: None}
                ]
            }
            
            documents_to_update = list(collection.find(query))
            
            if not documents_to_update:
                print(f"  No documents need updating in {collection_name}")
                continue
            
            print(f"  Found {len(documents_to_update)} documents to update")
            
            # Update each document
            updated_count = 0
            for doc in documents_to_update:
                if id_field in doc:
                    # Set target_field to the value of id_field
                    result = collection.update_one(
                        {"_id": doc["_id"]},
                        {"$set": {target_field: doc[id_field]}}
                    )
                    if result.modified_count > 0:
                        updated_count += 1
            
            print(f"  Successfully updated {updated_count} documents in {collection_name}")
            total_updated += updated_count
        
        print(f"\nTotal documents updated: {total_updated}")
        
        # Verify the fix by checking a few users
        print("\nVerification - checking first 3 users:")
        users_collection = db['users']
        sample_users = list(users_collection.find().limit(3))
        
        for user in sample_users:
            user_id = user.get('user_id', 'MISSING')
            _id = user.get('_id', 'MISSING')
            print(f"  User _id: {_id}, user_id: {user_id}")
        
        print("\nFix completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    fix_user_id_field()
