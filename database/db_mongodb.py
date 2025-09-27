import os
import json
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import logging

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            # Get MongoDB connection string from environment variable
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            database_name = os.getenv('MONGODB_DATABASE', 'telegram_bot')
            
            try:
                cls._instance.client = MongoClient(mongodb_uri)
                cls._instance.db = cls._instance.client[database_name]
                # Test the connection
                cls._instance.client.admin.command('ping')
                print(f"Connected to MongoDB database: {database_name}")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise
        return cls._instance
    
    def get_collection(self, collection_name):
        """
        Get a MongoDB collection wrapper that mimics the SQLite interface
        """
        return CollectionWrapper(self.db[collection_name])
    
    def get_next_id(self, collection_name):
        """
        Get the next ID for a collection (for compatibility with SQLite version)
        In MongoDB, ObjectId is typically used, but we can generate sequential IDs if needed
        """
        collection = self.db[collection_name]
        
        # For active_tasks, generate a unique string ID
        if collection_name == 'active_tasks':
            return f"task_{int(datetime.now().timestamp())}_{ObjectId()}"
        
        # For other collections, find the highest existing ID and increment
        try:
            last_doc = collection.find().sort("_id", -1).limit(1)
            last_doc = list(last_doc)
            if last_doc and isinstance(last_doc[0]["_id"], int):
                return last_doc[0]["_id"] + 1
            else:
                return 1
        except:
            return 1
    
    def close(self):
        if hasattr(self, 'client') and self.client:
            self.client.close()
            print("MongoDB connection closed.")

class CollectionWrapper:
    def __init__(self, collection):
        self.collection = collection
    
    def find_one(self, query=None):
        """
        Find a single document
        """
        try:
            result = self.collection.find_one(query or {})
            if result:
                # Convert ObjectId to string for compatibility
                if '_id' in result and isinstance(result['_id'], ObjectId):
                    result['_id'] = str(result['_id'])
            return result
        except Exception as e:
            print(f"Error in find_one: {e}")
            return None
    
    def find(self, query=None, limit=None, sort=None):
        """
        Find multiple documents
        """
        try:
            cursor = self.collection.find(query or {})
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)
            
            results = []
            for doc in cursor:
                # Convert ObjectId to string for compatibility
                if '_id' in doc and isinstance(doc['_id'], ObjectId):
                    doc['_id'] = str(doc['_id'])
                results.append(doc)
            return results
        except Exception as e:
            print(f"Error in find: {e}")
            return []
    
    def insert_one(self, document):
        """
        Insert a single document
        """
        try:
            # Handle the case where _id is provided as integer
            if '_id' in document and isinstance(document['_id'], int):
                # Keep the integer _id as is
                pass
            
            result = self.collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            print(f"Error in insert_one: {e}")
            return None
    
    def insert_many(self, documents):
        """
        Insert multiple documents
        """
        try:
            result = self.collection.insert_many(documents)
            return result.inserted_ids
        except Exception as e:
            print(f"Error in insert_many: {e}")
            return []
    
    def update_one(self, query, update, upsert=False):
        """
        Update a single document
        """
        try:
            # Handle MongoDB update operators
            if not any(key.startswith('$') for key in update.keys()):
                # If no MongoDB operators, wrap in $set
                update = {'$set': update}
            
            result = self.collection.update_one(query, update, upsert=upsert)
            return result.modified_count > 0 or (upsert and result.upserted_id is not None)
        except Exception as e:
            print(f"Error in update_one: {e}")
            return False
    
    def update_many(self, query, update):
        """
        Update multiple documents
        """
        try:
            # Handle MongoDB update operators
            if not any(key.startswith('$') for key in update.keys()):
                # If no MongoDB operators, wrap in $set
                update = {'$set': update}
            
            result = self.collection.update_many(query, update)
            return result.modified_count
        except Exception as e:
            print(f"Error in update_many: {e}")
            return 0
    
    def delete_one(self, query):
        """
        Delete a single document
        """
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error in delete_one: {e}")
            return False
    
    def delete_many(self, query):
        """
        Delete multiple documents
        """
        try:
            if not query:
                print("Error: delete_many called with empty query. Aborting.")
                return 0
            
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error in delete_many: {e}")
            return 0
    
    def count_documents(self, query=None):
        """
        Count documents matching the query
        """
        try:
            return self.collection.count_documents(query or {})
        except Exception as e:
            print(f"Error in count_documents: {e}")
            return 0

# Example usage (optional, for testing)
if __name__ == '__main__':
    # Set environment variables for testing
    # os.environ['MONGODB_URI'] = 'mongodb+srv://username:password@cluster.mongodb.net/'
    # os.environ['MONGODB_DATABASE'] = 'telegram_bot'
    
    try:
        db = Database()
        users = db.get_collection('users')
        
        # Example find
        user = users.find_one({'_id': 1})
        print("Found user:", user)
        
        all_users = users.find()
        print(f"Total users: {len(all_users)}")
        
        # Example count
        count = users.count_documents({})
        print("User count:", count)
        
        db.close()
    except Exception as e:
        print(f"Error during testing: {e}")
