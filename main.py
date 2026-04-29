# from fastapi import FastAPI,HTTPException,Request
# from database.db import engine, Base
# from routes import user_routes,cron_routes,product_routes
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse

# app = FastAPI()
# # CURRENCY = "₹"

# Base.metadata.create_all(bind=engine)

# app.include_router(user_routes.router)
# app.include_router(product_routes.router)  
# app.include_router(cron_routes.router)  
# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.exception_handler(HTTPException)
# async def auth_exception_handler(request: Request, exc: HTTPException):
#     if exc.status_code == 401:
#         response = RedirectResponse(url="/login")
#         response.delete_cookie("token")  # 🔥 important cleanup
#         return response
#     return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)



from fastapi import FastAPI, HTTPException, Request
from database import engine, Base
from routes import user_routes, cron_routes, product_routes
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os

app = FastAPI()

# ---------------- DB INIT (SAFE FOR RENDER) ----------------
try:
    Base.metadata.create_all(bind=engine)
    print("Database connected successfully")
except Exception as e:
    print("Database connection error:", e)

# ---------------- ROUTES ----------------
app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(cron_routes.router)

# ---------------- STATIC FILES (SAFE) ----------------
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- ERROR HANDLER ----------------
@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        response = RedirectResponse(url="/login")
        response.delete_cookie("token")
        return response
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

# ---------------- ROOT TEST ----------------
@app.get("/")
def home():
    return {"message": "FastAPI running on Render 🚀"}