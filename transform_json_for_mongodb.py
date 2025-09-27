
import json
import os
from datetime import datetime

def transform_users(users_data):
    transformed_users = []
    for user in users_data:
        # MongoDB typically uses _id. If user_id is unique and preferred, use it.
        # Otherwise, MongoDB will generate an ObjectId.
        # For now, we'll map user_id to _id and keep original user_id as sqlite_user_id
        user["_id"] = user.pop("user_id")
        user["sqlite_user_id"] = user["_id"]

        # Convert date strings to datetime objects if needed, or keep as strings
        for key in ["subscription_end", "created_at", "updated_at", "code_request_time"]:
            if user.get(key) and isinstance(user[key], str):
                try:
                    user[key] = datetime.fromisoformat(user[key])
                except ValueError:
                    pass # Keep as string if not a valid isoformat
        transformed_users.append(user)
    return transformed_users

def transform_responses(responses_data):
    transformed_responses = []
    for response in responses_data:
        response["_id"] = response.pop("id")
        response["sqlite_id"] = response["_id"]
        # user_id is a foreign key, will be referenced
        for key in ["created_at", "updated_at"]:
            if response.get(key) and isinstance(response[key], str):
                try:
                    response[key] = datetime.fromisoformat(response[key])
                except ValueError:
                    pass
        transformed_responses.append(response)
    return transformed_responses

def transform_subscriptions(subscriptions_data):
    transformed_subscriptions = []
    for sub in subscriptions_data:
        sub["_id"] = sub.pop("id")
        sub["sqlite_id"] = sub["_id"]
        # user_id and added_by are foreign keys
        if sub.get("created_at") and isinstance(sub["created_at"], str):
            try:
                sub["created_at"] = datetime.fromisoformat(sub["created_at"])
            except ValueError:
                pass
        transformed_subscriptions.append(sub)
    return transformed_subscriptions

def transform_sessions(sessions_data):
    transformed_sessions = []
    for session in sessions_data:
        session["_id"] = session.pop("id")
        session["sqlite_id"] = session["_id"]
        # user_id is a foreign key
        for key in ["created_at", "updated_at"]:
            if session.get(key) and isinstance(session[key], str):
                try:
                    session[key] = datetime.fromisoformat(session[key])
                except ValueError:
                    pass
        transformed_sessions.append(session)
    return transformed_sessions

def transform_groups(groups_data):
    transformed_groups = []
    for group in groups_data:
        group["_id"] = group.pop("id")
        group["sqlite_id"] = group["_id"]
        # user_id is a foreign key
        for key in ["created_at", "updated_at"]:
            if group.get(key) and isinstance(group[key], str):
                try:
                    group[key] = datetime.fromisoformat(group[key])
                except ValueError:
                    pass
        transformed_groups.append(group)
    return transformed_groups

def transform_posts(posts_data):
    transformed_posts = []
    for post in posts_data:
        post["_id"] = post.pop("id")
        post["sqlite_id"] = post["_id"]
        # group_ids is TEXT in SQLite, assuming it's a comma-separated string of IDs
        if post.get("group_ids") and isinstance(post["group_ids"], str):
            post["group_ids"] = [int(g_id) for g_id in post["group_ids"].split(",") if g_id.strip().isdigit()]
        else:
            post["group_ids"] = []

        for key in ["start_time", "created_at", "updated_at", "completed_at", "exact_time"]:
            if post.get(key) and isinstance(post[key], str):
                try:
                    post[key] = datetime.fromisoformat(post[key])
                except ValueError:
                    pass
        transformed_posts.append(post)
    return transformed_posts

def transform_messages(messages_data):
    transformed_messages = []
    for msg in messages_data:
        msg["_id"] = msg.pop("id")
        msg["sqlite_id"] = msg["_id"]
        # user_id and post_id are foreign keys
        if msg.get("timestamp") and isinstance(msg["timestamp"], str):
            try:
                msg["timestamp"] = datetime.fromisoformat(msg["timestamp"])
            except ValueError:
                pass
        transformed_messages.append(msg)
    return transformed_messages

def transform_active_tasks(active_tasks_data):
    transformed_tasks = []
    for task in active_tasks_data:
        # task_id is already TEXT PRIMARY KEY, can be used as _id or kept as is
        task["_id"] = task.pop("task_id")
        task["sqlite_task_id"] = task["_id"]
        # group_ids is TEXT, assuming comma-separated
        if task.get("group_ids") and isinstance(task["group_ids"], str):
            task["group_ids"] = [int(g_id) for g_id in task["group_ids"].split(",") if g_id.strip().isdigit()]
        else:
            task["group_ids"] = []

        for key in ["start_time", "last_activity", "exact_time"]:
            if task.get(key) and isinstance(task[key], str):
                try:
                    task[key] = datetime.fromisoformat(task[key])
                except ValueError:
                    pass
        transformed_tasks.append(task)
    return transformed_tasks

def transform_status_updates(status_updates_data):
    transformed_updates = []
    for update in status_updates_data:
        update["_id"] = update.pop("id")
        update["sqlite_id"] = update["_id"]
        # task_id is a foreign key (TEXT)
        if update.get("timestamp") and isinstance(update["timestamp"], str):
            try:
                update["timestamp"] = datetime.fromisoformat(update["timestamp"])
            except ValueError:
                pass
        transformed_updates.append(update)
    return transformed_updates

def transform_scheduled_posts(scheduled_posts_data):
    transformed_scheduled_posts = []
    for post in scheduled_posts_data:
        post["_id"] = post.pop("id")
        post["sqlite_id"] = post["_id"]
        for key in ["created_at", "updated_at"]:
            if post.get(key) and isinstance(post[key], str):
                try:
                    post[key] = datetime.fromisoformat(post[key])
                except ValueError:
                    pass
        transformed_scheduled_posts.append(post)
    return transformed_scheduled_posts

def transform_post_groups(post_groups_data):
    transformed_post_groups = []
    for pg in post_groups_data:
        pg["_id"] = pg.pop("id")
        pg["sqlite_id"] = pg["_id"]
        transformed_post_groups.append(pg)
    return transformed_post_groups

def transform_referrals(referrals_data):
    transformed_referrals = []
    for ref in referrals_data:
        ref["_id"] = ref.pop("id")
        ref["sqlite_id"] = ref["_id"]
        for key in ["created_at", "updated_at"]:
            if ref.get(key) and isinstance(ref[key], str):
                try:
                    ref[key] = datetime.fromisoformat(ref[key])
                except ValueError:
                    pass
        transformed_referrals.append(ref)
    return transformed_referrals

def transform_settings(settings_data):
    transformed_settings = []
    for setting in settings_data:
        setting["_id"] = setting.pop("id")
        setting["sqlite_id"] = setting["_id"]
        for key in ["created_at", "updated_at"]:
            if setting.get(key) and isinstance(setting[key], str):
                try:
                    setting[key] = datetime.fromisoformat(setting[key])
                except ValueError:
                    pass
        transformed_settings.append(setting)
    return transformed_settings


def main():
    input_dir = "Aloobohdaid/exported_json_data"
    output_dir = "Aloobohdaid/transformed_mongodb_data"
    os.makedirs(output_dir, exist_ok=True)

    transform_functions = {
        "users": transform_users,
        "responses": transform_responses,
        "subscriptions": transform_subscriptions,
        "sessions": transform_sessions,
        "groups": transform_groups,
        "posts": transform_posts,
        "messages": transform_messages,
        "active_tasks": transform_active_tasks,
        "status_updates": transform_status_updates,
        "scheduled_posts": transform_scheduled_posts,
        "post_groups": transform_post_groups,
        "referrals": transform_referrals,
        "settings": transform_settings,
    }

    for table_name, transform_func in transform_functions.items():
        input_file = os.path.join(input_dir, f"{table_name}.json")
        output_file = os.path.join(output_dir, f"{table_name}.json")

        if os.path.exists(input_file):
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            transformed_data = transform_func(data)

            with open(output_file, "w", encoding="utf-8") as f:
                # Use default=str for datetime objects during JSON serialization
                json.dump(transformed_data, f, ensure_ascii=False, indent=4, default=str)
            print(f"Transformed and saved {len(transformed_data)} records for {table_name} to {output_file}")
        else:
            print(f"Input file not found for {table_name}: {input_file}")

if __name__ == "__main__":
    main()

