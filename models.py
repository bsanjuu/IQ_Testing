from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Engineer(db.Model):
    __tablename__ = 'engineers'

    engineer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(50), default="Not Started")

    # Relationship to Execution
    executions = db.relationship('Execution', backref='engineer', lazy=True, cascade="all, delete-orphan")


class Checklist(db.Model):
    __tablename__ = 'checklists'

    checklist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(500))

    # Relationship to ChecklistItem
    items = db.relationship('ChecklistItem', backref='checklist', lazy=True, cascade="all, delete-orphan")

    # Relationship to Execution
    executions = db.relationship('Execution', backref='checklist', lazy=True, cascade="all, delete-orphan")


class ChecklistItem(db.Model):
    __tablename__ = 'checklist_items'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(500), nullable=False)
    executed = db.Column(db.Boolean, default=False)
    screenshot = db.Column(db.String(300), nullable=True)

    # Foreign key linking to Checklist
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.checklist_id'), nullable=False)
    executed_by = db.Column(db.String(100), nullable=True)  # Stores engineer’s name


class Execution(db.Model):
    """Tracks execution details for an IQ (checklist) by engineers."""
    __tablename__ = 'executions'

    execution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    engineer_id = db.Column(db.Integer, db.ForeignKey('engineers.engineer_id'), nullable=False)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.checklist_id'), nullable=False)
    status = db.Column(db.String(50), default="In Progress")
    executed_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def mark_completed(self):
        """Mark execution as completed."""
        self.status = "Completed"
