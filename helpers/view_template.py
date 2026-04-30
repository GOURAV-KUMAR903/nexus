from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
import constants

templates = Jinja2Templates(directory="templates")

# SAFE globals only (NO cache manipulation)
templates.env.globals.update({
    "APP_NAME": getattr(constants, "APP_NAME", ""),
    "VERSION": getattr(constants, "VERSION", ""),
})

def render_view(template_name: str, request: Request, context: dict = None) -> HTMLResponse:
    context = context or {}
    context["request"] = request
    return templates.TemplateResponse(template_name, context)