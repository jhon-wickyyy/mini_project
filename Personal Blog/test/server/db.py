import os
from config import DATA_FILE
import json

def load_users():
    file_path = os.path.join(DATA_FILE, 'users.json')

    with open(file_path,'r',encoding="utf-8") as f:
        users = json.load(f)

    return users if isinstance(users,list) else [users]

def load_articles():
    file_path = os.path.join(DATA_FILE, 'data.json')

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data if isinstance(data, list) else [data]

def save_articles(articles):
    file_path = os.path.join(DATA_FILE, 'data.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)