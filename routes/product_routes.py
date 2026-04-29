from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db import SessionLocal
from services import product_service
from fastapi import UploadFile, File, Form
from typing import Dict, Any, Optional


router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/add-product", response_class=HTMLResponse)
def product_form(request: Request):
    return product_service.addProduct(request)


@router.post("/add-product_post")
async def product_post(
    product_name: str = Form(...),
    product_brand: str = Form(...),
    product_category: str = Form(...),
    product_image: UploadFile = File(...),   
    product_description: str = Form(...),
    price: str = Form(...),
    db: Session = Depends(get_db)
):
    result = product_service.create_product(
        db, product_name, product_brand, product_category, product_description,product_image,price
    )
    # JSON response for JS
    return JSONResponse(content={"message": result["message"]})

@router.get("/product-details", response_class=HTMLResponse)
def product_details(request: Request):
    return product_service.product_page(request)

@router.post("/add-address")
def add_address(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    zip: str = Form(...)
):
    return product_service.add_address_logic(name, phone, address, city, zip)

@router.post("/create-order")
def add_order(
    request: Request,
    payment_method: str = Form(...),
    cart: str = Form(...),
    key: str = Form(..., alias="Secret")   # map Secret → key
):
    return product_service.order_placeholder(payment_method, cart,key)

@router.post("/addPaymentDetail")
def add_payment_detail(
    request: Request,
    payment_method: str = Form(...),
    # cart: str = Form(...),
    key: str = Form(..., alias="Secret"),
    cardNumber: str = Form(None),
    cardHolder: str = Form(None),
    expiry: str = Form(None),
    cvv: str = Form(None),
    upiId: str = Form(None)
):
    """
    Handles order creation for Card and UPI payments.
    cardNumber, cardHolder, expiry, cvv are required only for Card payments
    upiId is required only for UPI payments
    """
    return product_service.save_payment_detail(
        payment_method=payment_method,
        # cart=cart,
        key=key,
        cardNumber=cardNumber,
        cardHolder=cardHolder,
        expiry=expiry,
        cvv=cvv,
        upiId=upiId
    )
@router.get("/user-orders/{key}")
def user_orders(request: Request, key: str):
    return product_service.get_user_order_detail(request, key)
    
@router.get("/getOneproduct-detail/{orderId}")
def orders_detail(request: Request, orderId: int):
    return product_service.Getoneproduct_details(request, orderId)

@router.get("/tracking-detail/{Id}")
def track_detail(request: Request, Id: int):
    return product_service.trackproduct_details(request, Id)

@router.get("/getAddress/{addressId}")
def address_detail(request: Request, addressId: int):
    return product_service.getaddress_details(request, addressId)

