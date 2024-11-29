from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_setup import init_db, get_user_by_username, add_user
from s3_utils import upload_to_s3, list_s3_objects
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database setup
init_db()

# Home route
@app.route('/')
def index():
    if 'username' in session:
        files = list_s3_objects(os.getenv('S3_BUCKET_NAME', 'file-manager-bucket'))
        return render_template('index.html', username=session['username'], files=files)
    return redirect(url_for('login'))

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        return 'Invalid username or password'
    return render_template('login.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if get_user_by_username(username):
            return 'Username already exists'
        add_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

# File upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded'
    file = request.files['file']
    upload_to_s3(file, os.getenv('S3_BUCKET_NAME', 'file-manager-bucket'))
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
