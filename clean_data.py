import os
import json

UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'

def clean_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    folders_on_disk = set(os.listdir(UPLOAD_FOLDER))
    folders_in_data = set(data.keys())

    to_remove = folders_in_data - folders_on_disk

    if to_remove:
        for folder in to_remove:
            data.pop(folder)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)
        print(f"已删除无效记录: {to_remove}")
    else:
        print("无需清理，无无效记录。")

if __name__ == "__main__":
    clean_data()
