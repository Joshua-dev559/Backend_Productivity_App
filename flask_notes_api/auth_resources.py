from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, 
    set_access_cookies, 
    unset_jwt_cookies, 
    jwt_required, 
    get_jwt_identity
)
from app import db
from models import User

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data.get('username')).first():
            return {"message": "Username already exists"}, 400
        
        try:
            new_user = User(username=data.get('username'))
            new_user.set_password(data.get('password'))
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=str(new_user.id))
            response = {"message": "User created successfully", "user": {"id": new_user.id, "username": new_user.username}}
            return {"access_token": access_token, **response}, 201
        
        except ValueError as e:
               return {"message": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred during signup"}, 500
        

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and user.check_password(data.get('password')): 
          access_token = create_access_token(identity=str(user.id))
            
        return {
                "access_token": access_token,
                "user": {"id": user.id, "username": user.username}
        }, 200
        
        return {"message": "Invalid username or password"}, 401
    
class Logout(Resource):
    def post(self):
        return {"message": "Successfully logged out"}, 200
    
class Me(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user:
            return {"id": user.id, "username": user.username}, 200
        
        return {"message": "User not found"}, 404
