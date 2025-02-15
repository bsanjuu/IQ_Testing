[View Live](https://fastbootsanju.pythonanywhere.com/) 

# IQ Tracker

A Flask-based web application for managing and tracking execution of checklists by engineers.

---

## 🚀 Features
- ✅ **Create, Modify, and Execute Checklists**
- ✅ **Track Execution Status**
- ✅ **Upload Screenshots as Proof of Execution**
- ✅ **View Completed and Remaining Engineers**
- ✅ **Supports PostgreSQL and SQLite**

---

## 🛠️ Setup and Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/bsanjuu/IQ_Testing.git
cd IQ_Testing
```

### 2️⃣ Set Up a Virtual Environment
#### On macOS/Linux:
```sh
python3 -m venv .venv
source .venv/bin/activate
```
#### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Set Up the Database
```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🔄 Running the Application

### **For Local Development**
```sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
**or**
```sh
python app.py
```

### **For Production (Gunicorn)**
```sh
gunicorn app:app --workers 4 --bind 0.0.0.0:$PORT
```

---

## 📂 Project Structure
```
📦 IQ_Testing
 ┣ 📂 templates          # HTML templates
 ┣ 📂 static             # CSS, JavaScript, Images
 ┣ 📂 instance           # SQLite database (for local use)
 ┣ 📜 app.py             # Main Flask Application
 ┣ 📜 models.py          # Database Models
 ┣ 📜 insert_users.py    # Inserts Default Engineers
 ┣ 📜 insert_iqs.py      # Inserts Default Checklists
 ┣ 📜 requirements.txt   # Dependencies
 ┣ 📜 .gitignore         # Files to ignore in Git
 ┗ 📜 README.md          # Project Documentation
```

