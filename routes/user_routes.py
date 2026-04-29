from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db import SessionLocal
from services import user_service
from fastapi import Depends
from core.security import verify_jwt  # your JWT creation function
from typing import Dict, Any, Optional



router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_service.create_user(db, name,email,password)
    return RedirectResponse("/users", status_code=303)

@router.get("/users", response_class=HTMLResponse)
def show_users(
    request: Request,
    page: int = 1,
    db: Session = Depends(get_db),
    user_data: dict = Depends(verify_jwt)
):
    users, total_pages = user_service.get_all_users(db, page)
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
            "page": page,
            "total_pages": total_pages
        }
    )

@router.get("/shorten", response_class=HTMLResponse)
def shorten_get(request: Request):
    return user_service.ShortenURLService(request, templates)

# POST route → generate short URL
@router.post("/shorten", response_class=HTMLResponse)
def shorten_post(request: Request, original_url: str = Form(...)):
    return user_service.ShortenURLService(request, templates, original_url)

# Redirect route → click short URL
@router.get("/shorten_new/{short_code}")
def redirect_short_url(short_code: str):
    original_url = user_service.url_db.get(short_code)
    if original_url:
        return RedirectResponse(original_url)
    return {"error": "Short URL not found"}

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return user_service.UserVerfication(request)

from fastapi.responses import RedirectResponse

@router.post("/login_post")
async def login_post(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    result = user_service.UserVerficationPost(db, email, password)

    # ✅ If service already returns RedirectResponse → just return it
    if isinstance(result, RedirectResponse):
        return result

    # ❌ otherwise it's an error dict
    return result
    # return JSONResponse(content={"message": result["message"]})  # ✅ INSIDE
    
@router.get("/logout", response_class=HTMLResponse)
def login_form(request: Request):
    return user_service.logout(request)

@router.get("/new_register", response_class=HTMLResponse)
def login_form(request: Request):
    return user_service.register_new(request)

@router.post("/registerPost")
async def register_post(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    response = user_service.register_post(db, name , email, password)
    return response

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return user_service.dashboard(request)
