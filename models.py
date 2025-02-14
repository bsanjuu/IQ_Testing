from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Engineer(db.Model):
    engineer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ✅ Ensure auto-increment
    name = db.Column(db.String(100), nullable=False, unique=True)  # ✅ Enforce unique names
    status = db.Column(db.String(50), default="Not Started")  # ✅ Track execution status

    # ✅ Relationship to executed checklists
    executions = db.relationship('Execution', backref='engineer', lazy=True)


class Checklist(db.Model):
    checklist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ✅ Changed 'id' to 'checklist_id'
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(500))
    items = db.relationship('ChecklistItem', backref='checklist', lazy=True,
                            cascade="all, delete-orphan")  # ✅ Cascade delete items if checklist is deleted
    executions = db.relationship('Execution', backref='checklist',
                                 lazy=True)  # ✅ Track which engineers executed this IQ


class ChecklistItem(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ✅ Changed 'id' to 'item_id'
    description = db.Column(db.String(500), nullable=False)
    executed = db.Column(db.Boolean, default=False)
    screenshot = db.Column(db.String(300))

    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist.checklist_id'),
                             nullable=False)  # ✅ FK linking to Checklist
    executed_by = db.Column(db.String(100))  # ✅ Stores engineer’s name who executed the task

class Execution(db.Model):
    """Tracks execution details for an IQ (checklist) by engineers."""
    execution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    engineer_id = db.Column(db.Integer, db.ForeignKey('engineer.engineer_id'), nullable=False)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist.checklist_id'), nullable=False)
    status = db.Column(db.String(50), default="In Progress")  # Tracks execution status
    executed_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp

    def mark_completed(self):
        self.status = "Completed"
