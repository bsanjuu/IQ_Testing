from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

from models import db, Engineer, Checklist, ChecklistItem, Execution  # Import models

# ✅ Initialize Flask App
app = Flask(__name__)

# ✅ Configure Database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'checklists.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')

# ✅ Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ✅ Initialize Database & Migration
db.init_app(app)
migrate = Migrate(app, db)

# ✅ Insert default data into the database (Fixed Circular Import)
with app.app_context():
    db.create_all()

    from insert_users import insert_engineers
    from insert_iqs import insert_iqs

    insert_engineers()  # Insert engineers on startup
    insert_iqs()  # Insert checklists on startup


# ✅ Serve Uploaded Files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ✅ Main Routes
@app.route('/')
def index():
    checklists = Checklist.query.all()
    return render_template('index.html', checklists=checklists)


@app.route('/create_iq', methods=['GET', 'POST'])
def create_iq():
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        items = request.form.getlist('items[]')

        existing_checklist = Checklist.query.filter_by(name=name).first()
        if existing_checklist:
            return "Error: A checklist with this name already exists!", 400

        new_checklist = Checklist(name=name, description=description)
        db.session.add(new_checklist)
        db.session.commit()

        for item_desc in items:
            if item_desc.strip():
                checklist_item = ChecklistItem(description=item_desc, checklist_id=new_checklist.checklist_id)
                db.session.add(checklist_item)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_iq.html')


@app.route('/modify_iq', methods=['GET', 'POST'])
def modify_iq():
    checklists = Checklist.query.all()
    selected_checklist_id = request.args.get('checklist_id', type=int) or request.form.get('selected_checklist',
                                                                                           type=int)
    checklist = Checklist.query.get(selected_checklist_id) if selected_checklist_id else None

    if request.method == 'POST':
        action = request.form.get('action')

        if not checklist:
            return "Error: No checklist selected!", 400

        if action == 'add_item':
            new_item_desc = request.form['new_item'].strip()
            if new_item_desc:
                db.session.add(ChecklistItem(description=new_item_desc, checklist_id=checklist.checklist_id))
                db.session.commit()

        elif action == 'edit_item':
            item_id = request.form['item_id']
            new_desc = request.form['edit_desc'].strip()
            item = ChecklistItem.query.get(item_id)
            if item:
                item.description = new_desc
                db.session.commit()

        elif action == 'delete_item':
            item_id = request.form['item_id']
            item = ChecklistItem.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()

        return redirect(url_for('modify_iq', checklist_id=checklist.checklist_id))

    return render_template('modify_iq.html', checklists=checklists, checklist=checklist)


@app.route('/execute_iq', methods=['GET', 'POST'])
def execute_iq():
    checklists = Checklist.query.all()
    engineers = Engineer.query.all()

    checklist_id = request.args.get('checklist_id', type=int)
    checklist = Checklist.query.get(checklist_id) if checklist_id else None

    if request.method == 'POST':
        engineer_id = request.form.get('selected_engineer')

        if not checklist_id or not engineer_id:
            return "Error: Engineer ID or Checklist ID is missing", 400

        engineer = Engineer.query.get(engineer_id)
        if not engineer or not checklist:
            return "Error: Selected checklist or engineer does not exist", 400

        # ✅ Ensure only ONE folder per checklist (IQ)
        iq_folder = os.path.join(app.config['UPLOAD_FOLDER'], f"IQ_{checklist.checklist_id}")
        os.makedirs(iq_folder, exist_ok=True)

        # ✅ Each engineer gets a subfolder inside the IQ folder
        engineer_folder = os.path.join(iq_folder, engineer.name.replace(" ", "_"))
        os.makedirs(engineer_folder, exist_ok=True)

        completed_all_items = True

        for item in checklist.items:
            executed = request.form.get(f'execute_{item.item_id}') == 'Yes'
            file = request.files.get(f'screenshot_{item.item_id}')

            if file and file.filename:
                screenshot_filename = secure_filename(file.filename)
                file_path = os.path.join(engineer_folder, screenshot_filename)
                file.save(file_path)

                relative_path = os.path.relpath(file_path, app.config['UPLOAD_FOLDER'])
                item.screenshot = relative_path

            item.executed = executed
            item.executed_by = engineer.name if executed else None

            if not executed:
                completed_all_items = False

        # ✅ Insert or update Execution Record
        execution_record = Execution.query.filter_by(engineer_id=engineer_id, checklist_id=checklist_id).first()

        if not execution_record:
            execution_record = Execution(
                engineer_id=engineer_id, checklist_id=checklist_id,
                status="Completed" if completed_all_items else "In Progress"
            )
            db.session.add(execution_record)
        else:
            execution_record.status = "Completed" if completed_all_items else "In Progress"

        engineer.status = "Completed" if completed_all_items else "In Progress"

        db.session.commit()
        return redirect(url_for('execute_iq', checklist_id=checklist_id))

    return render_template('execute_iq.html', checklists=checklists, engineers=engineers, checklist=checklist)


@app.route('/executed_engineers')
def executed_engineers():
    checklists = Checklist.query.all()
    selected_checklist_id = request.args.get('checklist_id', type=int)

    executed = []
    remaining = []

    if selected_checklist_id:
        selected_checklist = Checklist.query.get(selected_checklist_id)

        executed = Engineer.query.join(Execution).filter(
            Execution.checklist_id == selected_checklist_id,
            Execution.status == "Completed"
        ).all()

        remaining = Engineer.query.filter(
            ~Engineer.engineer_id.in_([e.engineer_id for e in executed])
        ).all()

        return render_template('executed_engineers.html', checklists=checklists, executed=executed,
                               remaining=remaining, selected_checklist_id=selected_checklist_id,
                               selected_checklist=selected_checklist)

    return render_template('executed_engineers.html', checklists=checklists, executed=[], remaining=[],
                           selected_checklist_id=None, selected_checklist=None)


@app.route('/executed_data')
def executed_data():
    checklist_id = request.args.get('checklist_id', type=int)

    executed_count = Execution.query.filter_by(checklist_id=checklist_id, status="Completed").count()
    remaining_count = Engineer.query.filter(
        Engineer.engineer_id.notin_(
            Execution.query.with_entities(Execution.engineer_id).filter_by(checklist_id=checklist_id)
        )
    ).count()

    return jsonify({"executed_count": executed_count, "remaining_count": remaining_count})


if __name__ == '__main__':
    app.run(debug=True)
