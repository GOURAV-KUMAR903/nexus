from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
import constants   # <-- ye line add karo

# Initialize templates folder
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(vars(constants))


def render_view(template_name: str, request: Request, context: dict = None) -> HTMLResponse:
    context = context or {}
    context.update({"request": request})
    return templates.TemplateResponse(template_name, context)