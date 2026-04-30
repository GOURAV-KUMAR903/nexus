from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session

from database.db import SessionLocal
from services import user_service
from core.security import verify_jwt
from helpers.view_template import render_view

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def register_form(request: Request):
    return render_view("register.html", request, {})


@router.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_service.create_user(db, name, email, password)
    return RedirectResponse("/users", status_code=303)


@router.get("/users", response_class=HTMLResponse)
def show_users(
    request: Request,
    page: int = 1,
    db: Session = Depends(get_db),
    user_data: dict = Depends(verify_jwt)
):
    users, total_pages = user_service.get_all_users(db, page)

    return render_view(
        "users.html",
        request,
        {
            "users": users,
            "page": page,
            "total_pages": total_pages
        }
    )


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return render_view("new_login.html", request, {})


@router.post("/login_post")
def login_post(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    result = user_service.UserVerficationPost(db, email, password)

    if isinstance(result, RedirectResponse):
        return result

    return JSONResponse(content=result)


@router.get("/logout")
def logout():
    return user_service.logout()


@router.get("/new_register", response_class=HTMLResponse)
def new_register(request: Request):
    return render_view("register1.html", request, {})


@router.post("/registerPost")
def register_post(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return user_service.register_post(db, name, email, password)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return render_view("index.html", request, {})