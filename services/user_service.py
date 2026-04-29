from models.user_model import User
from helpers.view_template import render_view
from constants import CURRENCY, BASE_URL  # import constants
from helpers.super_helper import SuperHelper
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import os
from fastapi import Request
import random
import string
from cryptography.fernet import Fernet,InvalidToken
from fastapi.responses import RedirectResponse  # ✅ THIS IS REQUIRED
from core.security import create_access_token  # your JWT creation function
from fastapi.responses import JSONResponse

# key = Fernet.generate_key()
load_dotenv()  
key = os.getenv("SECRET_KEY")
cipher_suite = Fernet(key)
url_db = {}
sessions = {} 



def create_user(db, name,email, password):
    encMessage = cipher_suite.encrypt(password.encode())
    user = User(name=name ,email= email, password=encMessage)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# def get_all_users(db):
#     return db.query(User).all()
def get_all_users(db, page: int = 1, page_size: int = 10):
    total = db.query(User).count()
    offset = (page - 1) * page_size

    users = db.query(User).offset(offset).limit(page_size).all()

    for user in users:
        decrypted = cipher_suite.decrypt(user.password)
        user.password = decrypted.decode('utf-8')
      
    total_pages = (total + page_size - 1) // page_size

    return users, total_pages

def login_user(db, name, password):
    return db.query(User).filter(
        User.name == name,
        User.password == password
    ).first()
    
def UserVerfication(request: Request):
    
    return render_view(
     "new_login.html",
     request,
     {
     }
    )


def UserVerficationPost(db, email: str, password: str):
    User = SuperHelper.get_single_record("users", {"email": email}, "*")
    
    if not User:
        return {"message": "Invalid credentials"}
    
    decryptPassword = cipher_suite.decrypt(User['password']).decode('utf-8')
    
    if User["email"] == email and decryptPassword == password:
        token_data = {"user_id": User["id"], "email": User["email"]}
        session_token = create_access_token(token_data)
        
        # ✅ Redirect instead of JSONResponse
        response = RedirectResponse(url="/users", status_code=302)
        
        # ✅ Set cookie properly
        response.set_cookie(
            key="token",
            value=session_token,
            httponly=True
        )
        
        return response
    else:
        return {"message": "Invalid credentials"}
    
    

def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=302)
    
    # ✅ must match login cookie name
    response.delete_cookie("token")
    
    return response

def register_new(request: Request):
    return render_view(
     "register1.html",
     request,
     {
     }
    )
    
def register_post(request: Request, name : str , email: str , password : str):
     
    Encrypt_pass = cipher_suite.encrypt(password.encode())
    record_data = {
            "name": name,
            "email": email,
            "password": Encrypt_pass,
        }
    inserted_id = SuperHelper.add("users", record_data)    
    return {"message": "User registered successfully"}

def dashboard(request: Request):
     return render_view(
     "index.html",
     request,
     {
     }
    )
    
    
    
    
    
 
    