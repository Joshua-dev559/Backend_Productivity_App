from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from models import User, Note
from auth_resources import Signup, Login, Logout, Me
from note_resources import NoteListResource, NoteResource

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Me, '/me')

api.add_resource(NoteListResource, '/notes')
api.add_resource(NoteResource, '/notes/<int:note_id>')

@app.route('/')
def index():
    return {"message": "Productivity Backend API is running!"}

if __name__ == '__main__':
    app.run(debug=True)
    