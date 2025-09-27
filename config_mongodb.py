import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'telegram_bot')

# Telegram Bot Configuration (keep existing)
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
API_ID = os.getenv('API_ID', '')
API_HASH = os.getenv('API_HASH', '')

# Other configurations
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

def get_mongodb_config():
    """
    Get MongoDB configuration
    """
    return {
        'uri': MONGODB_URI,
        'database': MONGODB_DATABASE
    }

def validate_mongodb_config():
    """
    Validate that required MongoDB configuration is present
    """
    if not MONGODB_URI or MONGODB_URI == 'mongodb://localhost:27017/':
        print("Warning: MONGODB_URI not set or using default localhost")
        return False
    
    if not MONGODB_DATABASE:
        print("Warning: MONGODB_DATABASE not set")
        return False
    
    return True

if __name__ == "__main__":
    print("MongoDB Configuration:")
    print(f"URI: {MONGODB_URI}")
    print(f"Database: {MONGODB_DATABASE}")
    print(f"Valid: {validate_mongodb_config()}")
