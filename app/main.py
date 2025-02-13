from flask import Flask, render_template, request, redirect, session, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from utils import init_db, get_user_by_username, add_user, upload_to_s3, list_s3_objects, get_s3_object
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecret')

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
        password = generate_password_hash(request.form['password'], 'pbkdf2')
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

# Download File
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_obj = get_s3_object(filename, os.getenv('S3_BUCKET_NAME', 'file-manager-bucket'))
    if not file_obj:
        return 'File not found', 404
    file_content = file_obj['Body'].read()
    return send_file(BytesIO(file_content), as_attachment=True, download_name=filename)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))