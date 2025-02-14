from app import app, db
from models import Checklist, ChecklistItem

# List of IQ Checklists to insert
iq_checklists = [
    {
        "name": "Software Installation IQ",
        "description": "Checklist for software installation verification",
        "items": [
            "Download the installer",
            "Run setup wizard",
            "Accept terms and conditions",
            "Verify successful installation"
        ]
    },
    {
        "name": "System Configuration IQ",
        "description": "Checklist for configuring the system",
        "items": [
            "Set up environment variables",
            "Configure firewall rules",
            "Verify network connectivity",
            "Run system diagnostics"
        ]
    },
    {
        "name": "Security Compliance IQ",
        "description": "Checklist for verifying security compliance",
        "items": [
            "Enable 2FA",
            "Configure secure passwords",
            "Update security patches",
            "Perform vulnerability scan"
        ]
    }
]

def insert_iqs():
    """Insert IQ checklists and their items into the database."""
    with app.app_context():
        for checklist_data in iq_checklists:
            existing_checklist = Checklist.query.filter_by(name=checklist_data["name"]).first()
            if not existing_checklist:
                checklist = Checklist(name=checklist_data["name"], description=checklist_data["description"])
                db.session.add(checklist)
                db.session.commit()  # Commit first to get the checklist_id

                # Insert checklist items
                items = [
                    ChecklistItem(description=item_desc, checklist_id=checklist.checklist_id)
                    for item_desc in checklist_data["items"]
                ]
                db.session.add_all(items)

        db.session.commit()
        print("✅ IQ Checklists inserted successfully!")

if __name__ == "__main__":
    insert_iqs()
