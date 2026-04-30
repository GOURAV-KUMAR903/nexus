from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
import constants

templates = Jinja2Templates(directory="templates")

templates.env.globals.update({
    "APP_NAME": getattr(constants, "APP_NAME", None),
    "VERSION": getattr(constants, "VERSION", None),
})

# optional debug safety
templates.env.cache = {}

def render_view(template_name: str, request: Request, context: dict = None) -> HTMLResponse:
    context = context or {}
    context["request"] = request
    return templates.TemplateResponse(template_name, context)