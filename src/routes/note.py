from flask import Blueprint, jsonify, request
from src.models.note import Note, db

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note. Return can_delete=False so frontend hides delete button until list refresh."""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        title = data['title'].strip()
        if len(title) > 30:
            return jsonify({'error': 'Title should be less than 30 characters'}), 400

        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()

        resp = note.to_dict()
        resp['can_delete'] = False  # explicitly mark newly created note as non-deletable (UI purpose only)
        return jsonify(resp), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    d = note.to_dict()
    d['can_delete'] = True  # existing notes can be deleted
    return jsonify(d)

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if 'title' in data and data['title'] is not None:
            new_title = data['title'].strip()
            if len(new_title) > 30:
                return jsonify({'error': 'Title should be less than 30 characters'}), 400
            note.title = new_title or note.title
        note.content = data.get('content', note.content)
        db.session.commit()
        d = note.to_dict()
        d['can_delete'] = True
        return jsonify(d)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()

    results = []
    for n in notes:
        d = n.to_dict()
        d['can_delete'] = True
        results.append(d)
    return jsonify(results)

