
import sqlite3
import json
import os
from datetime import datetime

def export_table_to_json(db_path, table_name, output_dir):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row # This allows accessing columns by name
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        data = []
        for row in rows:
            row_dict = dict(row)
            # Convert datetime objects to ISO format strings if present
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = value.isoformat()
            data.append(row_dict)

        output_file = os.path.join(output_dir, f"{table_name}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Exported {len(data)} records from {table_name} to {output_file}")

    except sqlite3.Error as e:
        print(f"Error exporting table {table_name}: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    sqlite_db_path = "Aloobohdaid/data/telegram_bot.db"
    output_directory = "Aloobohdaid/exported_json_data"

    os.makedirs(output_directory, exist_ok=True)

    # List of tables to export, based on the schema analysis
    tables = [
        "users", "responses", "subscriptions", "sessions", "groups",
        "posts", "messages", "active_tasks", "status_updates",
        "scheduled_posts", "post_groups", "referrals", "settings"
    ]

    for table in tables:
        export_table_to_json(sqlite_db_path, table, output_directory)


