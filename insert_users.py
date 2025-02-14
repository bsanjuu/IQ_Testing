from app import app, db
from models import Engineer

# List of engineers to insert
engineers = [
    {"engineer_id": 1, "name": "Rishika Demi"},
    {"engineer_id": 2, "name": "Sanjeevlu Buggargani"},
    {"engineer_id": 3, "name": "Aarav Sharma"},
    {"engineer_id": 4, "name": "Neha Verma"},
    {"engineer_id": 5, "name": "Rahul Reddy"},
    {"engineer_id": 6, "name": "Priya Nair"},
    {"engineer_id": 7, "name": "Vikram Choudhary"},
    {"engineer_id": 8, "name": "Ananya Iyer"},
    {"engineer_id": 9, "name": "Rohan Patil"},
    {"engineer_id": 10, "name": "Deepika Raj"}
]

def insert_engineers():
    """Insert engineers into the database only if they do not already exist."""
    with app.app_context():  # ✅ Ensures database operations run inside Flask context
        for engineer_data in engineers:
            existing_engineer = Engineer.query.filter_by(name=engineer_data["name"]).first()

            if not existing_engineer:  # Avoid duplicates
                engineer = Engineer(name=engineer_data["name"])  # ✅ No need to set engineer_id manually
                db.session.add(engineer)

        db.session.commit()
        print("✅ Engineers inserted successfully!")

if __name__ == "__main__":
    insert_engineers()
