from app import db, bycrypt
from sqlalchemy.orm import validates
import requests

class User(db.model):
    __tablename__ = 'users'
    id = db.column(db.Integer, primary_key=True)
    username = db.Column(db.string(80), unique=True, nullable=False)
    password_harsh = db.Column(db.String(125), nullable=False)
    
    notes = db.relationship('Note', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required")
        if len(username) < 4:
            raise ValueError("Username must be at least 4 characters long")
        return username

    def __repr__(self):
        return f'<User {self.username}>'
    

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title is required")
        return title

    def to_dict(self):
         return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f'<Note {self.title}>'