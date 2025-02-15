import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ✅ Initialize Flask App
app = Flask(__name__)

# ✅ Ensure `instance` directory exists for SQLite database storage
INSTANCE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

# ✅ Ensure `uploads` directory exists
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Configure Database (Store SQLite file in the `instance` directory)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(INSTANCE_DIR, 'checklists.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set upload folder path

# ✅ Initialize Database
db = SQLAlchemy(app)
