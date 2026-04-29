from fastapi import FastAPI, HTTPException, Request
from database.db import engine, Base
from routes import user_routes, cron_routes, product_routes
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI()
templates.env.cache = {}
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(cron_routes.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        response = RedirectResponse(url="/login")
        response.delete_cookie("token")
        return response
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)