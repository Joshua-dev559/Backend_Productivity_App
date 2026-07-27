from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Note

class NoteListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        pagination = Note.query.filter_by(user_id=current_user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        notes = [note.to_dict() for note in pagination.items]
        return {
            "notes": notes,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "next_page": pagination.next_num,
            "prev_page": pagination.prev_num
        }, 200

    @jwt_required()
    def post(self):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        try:
            new_note = Note(
                title=data.get('title'),
                content=data.get('content'),
                user_id=current_user_id
            )
            
            db.session.add(new_note)
            db.session.commit()
            
            return new_note.to_dict(), 201
            
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": "Could not create note"}, 500
        
class NoteResource(Resource):
    @jwt_required()
    def get(self, note_id):
        current_user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
        
        if not note:
            return {"message": "Note not found or unauthorized"}, 404
            
        return note.to_dict(), 200

    @jwt_required()
    def patch(self, note_id):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
        
        if not note:
            return {"message": "Note not found or unauthorized"}, 404
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
            
        try:
            db.session.commit()
            return note.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Could not update note"}, 500

    @jwt_required()
    def delete(self, note_id):
        current_user_id = int(get_jwt_identity())
        
        note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
        
        if not note:
            return {"message": "Note not found or unauthorized"}, 404
            
        try:
            db.session.delete(note)
            db.session.commit()
            return {"message": "Note deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Could not delete note"}, 500
        