import json

def save_chat_history(chat_history, file_path="chat_history.json"):
    """
    Saves the chat history to a JSON file.
    Args:
        chat_history (list): List of message dicts (role/content).
        file_path (str): Path to the JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)
    print(f"✅ chat_history saved to {file_path}")

def load_chat_history(file_path="chat_history.json"):
    """
    Loads the chat history from a JSON file.
    Returns an empty list if the file does not exist or is empty.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print("⚠️ chat_history.json is not a list. Returning empty list.")
                return []
    except FileNotFoundError:
        print(f"⚠️ {file_path} not found. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"⚠️ {file_path} is empty or not valid JSON. Returning empty list.")
        return []
