import os
import re

def update_database_imports(file_path):
    """
    Update database imports from SQLite to MongoDB version
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace import statements
        original_content = content
        
        # Replace "from database.db_mongodb import Database" with "from database.db_mongodb import Database"
        content = re.sub(
            r'from database\.db import Database',
            'from database.db_mongodb import Database',
            content
        )
        
        # Replace "import database.db_mongodb" with "import database.db_mongodb_mongodb"
        content = re.sub(
            r'import database\.db',
            'import database.db_mongodb_mongodb',
            content
        )
        
        # If content was changed, write it back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated imports in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def find_and_update_files(directory):
    """
    Find all Python files that import database.db_mongodb and update them
    """
    updated_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip .local and other irrelevant directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Check if file contains database.db import
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'from database.db import' in content or 'import database.db_mongodb' in content:
                        if update_database_imports(file_path):
                            updated_files.append(file_path)
                            
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return updated_files

def main():
    # Update imports in the Aloobohdaid directory
    directory = "Aloobohdaid"
    
    print("Searching for files with database.db imports...")
    updated_files = find_and_update_files(directory)
    
    if updated_files:
        print(f"\nSuccessfully updated {len(updated_files)} files:")
        for file_path in updated_files:
            print(f"  - {file_path}")
    else:
        print("No files needed updating.")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
