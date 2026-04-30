from models.user_model import User
from helpers.super_helper import SuperHelper
from cryptography.fernet import Fernet
from fastapi.responses import RedirectResponse
from core.security import create_access_token
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("SECRET_KEY")
cipher_suite = Fernet(key)


def create_user(db, name, email, password):
    enc = cipher_suite.encrypt(password.encode())
    user = User(name=name, email=email, password=enc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db, page: int = 1, page_size: int = 10):
    total = db.query(User).count()
    offset = (page - 1) * page_size

    users = db.query(User).offset(offset).limit(page_size).all()

    for u in users:
        u.password = cipher_suite.decrypt(u.password).decode()

    total_pages = (total + page_size - 1) // page_size
    return users, total_pages


def UserVerficationPost(db, email: str, password: str):
    user = SuperHelper.get_single_record("users", {"email": email}, "*")

    if not user:
        return {"message": "Invalid credentials"}

    decrypted = cipher_suite.decrypt(user["password"]).decode()

    if decrypted == password:
        token = create_access_token({
            "user_id": user["id"],
            "email": user["email"]
        })

        response = RedirectResponse("/users", status_code=302)
        response.set_cookie("token", token, httponly=True)
        return response

    return {"message": "Invalid credentials"}


def logout():
    response = RedirectResponse("/login")
    response.delete_cookie("token")
    return response


def register_post(db, name, email, password):
    enc = cipher_suite.encrypt(password.encode())

    SuperHelper.add("users", {
        "name": name,
        "email": email,
        "password": enc
    })

    return {"message": "User registered successfully"}