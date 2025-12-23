from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        notes = request.form.get('notes')

        if len(notes) < 1:
            flash('Notes is too short!', category = 'error')
        else:
            new_notes = Note(data = notes, user_id = current_user.id)
            db.session.add(new_notes)
            db.session.commit()
            flash('notes is added', category = 'success')
    return render_template("home.html", user = current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user = current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data)
    note_id = data.get('noteId')

    note = Note.query.get(note_id)

    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    return jsonify({})