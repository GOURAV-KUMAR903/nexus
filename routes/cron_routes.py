from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db import SessionLocal
from services import Cron_service
from fastapi import UploadFile, File, Form

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/deleteCron")
def DeleteCron(request: Request):
    return Cron_service.Autodelete_Cron(request)