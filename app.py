from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import json
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 随便写一个即可，用于闪现消息

UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    return to_remove

@app.route('/')
def index():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    folders = list(data.keys())
    return render_template('index.html', folders=folders)

@app.route('/clean')
def clean():
    removed = clean_data()
    if removed:
        flash(f"已删除无效记录: {', '.join(removed)}")
    else:
        flash("无需清理，无无效记录。")
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        password = request.form['password']
        if file:
            folder_id = str(uuid.uuid4())[:8]
            folder_path = os.path.join(UPLOAD_FOLDER, folder_id)
            os.makedirs(folder_path, exist_ok=True)
            filepath = os.path.join(folder_path, file.filename)
            file.save(filepath)

            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            data[folder_id] = {'filename': file.filename, 'password': password}
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f)

            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/view/<folder_id>', methods=['GET', 'POST'])
def view(folder_id):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    if folder_id not in data:
        return "文件夹不存在。"

    if request.method == 'POST':
        password = request.form['password']
        if password == data[folder_id]['password']:
            return send_from_directory(os.path.join(UPLOAD_FOLDER, folder_id), data[folder_id]['filename'])
        else:
            return "密码错误。"

    return render_template('view.html', folder_id=folder_id)

if __name__ == '__main__':
    app.run(debug=True)
