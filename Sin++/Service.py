from flask import (Flask, render_template, request,
                    jsonify, url_for, send_from_directory,
                   current_app, send_file)
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder="html", static_folder="upload")
app.config['UPLOAD_FOLDER'] = 'upload'

# 显示原图和上一次图片
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hello')
def hello():
    return 'Hello, Flask'


@app.route('/user/<username>')
def user(username):
    return render_template("hello.html", name=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do login business'
    else:
        return 'show login form'


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['new_file']
        file.save('upload/'+secure_filename(file.filename))
        return "OK"
    else:
        return render_template('upload.html')


@app.route('/download_file')
def download_file():
    return render_template('download.html')

# 可行
@app.route('/upload/<filename>')
def upload(filename=None):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

# 有问题
@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename)
    print(path)
    return app.send_static_file(path)

# json format
@app.route('/me')
def me_api():
    user = {'username':'hujun', 'theme':'black'}
    return {
        "username": user.username,
        "theme": user.theme,
    }


@app.route("/users")
def users_api():
    users = {'username':'hujun', 'theme':'black'}
    return jsonify([user.to_json() for user in users])


@app.route("/token")
def token():
    request.path="https://open.ys7.com/api/lapp/token/get?appKey=c127ab47d5dc450088b7c9ce8a8aac85&appSecret=9316c6d3ece1d67e7eb8b386fb365fb5"
    request.method = 'POST'
    return request.get_json()


if __name__ == '__main__':
    print("service start run")
    app.run(host="localhost", port=9099)