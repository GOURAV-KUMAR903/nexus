from models.product_model import Product
from helpers.save_image import save_img
from helpers.view_template import render_view
from fastapi import UploadFile
from helpers.super_helper import SuperHelper
from fastapi import Request
from fastapi.encoders import jsonable_encoder
import random
import json
from fastapi import FastAPI
import os
import secrets  # <-- add this at the top
from constants import CURRENCY, BASE_URL  # import constants

app = FastAPI()

# Serve static files at URL /static



def addProduct(request: Request):
    return render_view(
        "product.html",
        request,
        {
        }
    )
    
# def create_product(db, product_name, product_brand,product_category,product_description,product_image,price):
#     image_path = save_img(product_image) if product_image else None
#     product_rating = random.uniform(0, 5),
#     product_detail = Product(product_name = product_name, product_brand = product_brand ,product_category = product_category,product_description = product_description,product_image = image_path, price = price,product_rating = product_rating)
#     db.add(product_detail)
#     db.commit()
#     db.refresh(product_detail)
#     return {"product": product_detail, "message": "Product added successfully!"}

def create_product(db,product_name, product_brand, product_category, product_description, product_image, price):
    image_path = save_img(product_image) if product_image else None
    product_rating = random.uniform(0, 5)
    product_instance = {
        "product_name" : product_name,
        "product_brand" : product_brand,
        "product_category" : product_category,
        "product_description" : product_description,
        "product_image":image_path,
        "price" : price,
        "product_rating" : product_rating
    }
    result = SuperHelper.add('product', product_instance)
    if result :
        return {"message": "Product added successfully!"}
    else:
        return {"message": "Something Went Wrong!"}



def product_page(request: Request):
    all_products = SuperHelper.get_records("product")
    products_json = json.dumps(jsonable_encoder(all_products))
    return render_view(
        "product_details.html",
        request,
        {
            "title": "Product Details",
            "products_json": products_json,  # <-- Use a unique name
            "base_url": BASE_URL,
            "CURRENCY": CURRENCY
        }
    )
def add_address_logic(name: str, phone: str, address: str, city: str, zip: str):
    secret_key = generate_secret_key_for_order()  # 32-char hex key
    record_partial = SuperHelper.get_single_record("tbl_addresses", {"secret_key": secret_key}, "*")
    record_phone = SuperHelper.get_single_record("tbl_addresses", {"phone": phone }, "*")
    if record_phone:
        return {"status": "error", "message": "This phone already has an address"}
    if not record_partial:
        addres = address.replace(" ", "")
        address_data = {
            "name": name,
            "phone": phone,
            "address": addres,
            "city": city,
            "zip": zip,
            "secret_key": secret_key
        }
        inserted_id = SuperHelper.add("tbl_addresses", address_data)
        if inserted_id:
            return {"status": "success", "message": "Address saved", "secret_key": secret_key}
        else:
            return {"status": "error", "message": "Failed to save address"}  
    else:    
       return {"status": "error", "message": "Duplicate key match !"}  

def order_placeholder(payment_method, cart, key):
    cart_items = json.loads(cart)
    getSecretKey = SuperHelper.get_single_record("tbl_addresses", {"secret_key": key}, "*")
    if not getSecretKey:
        return {"status": "error", "message": "Private Key is Not Match Please Try Again !"}
    orders = []
    for item in cart_items:
        product_id = item["id"]
        quantity = item["quantity"]
        getproduct_detail = SuperHelper.get_single_record("product", {"id": product_id}, "*")
        if not getproduct_detail:
            return {"status": "error", "message": f"Product {product_id} not found !"}
        price = getproduct_detail['price'] * quantity
        order_data = {
            "secret_key": getSecretKey['secret_key'],
            "order_id": getproduct_detail['id'],
            "address_id": getSecretKey['id'],
            "quantity": quantity,
            "price": price,
            "payment_method": payment_method,
            "status": 1
        }
        inserted_id = SuperHelper.add("tbl_orders", order_data)

        # print(order_data)
        orders.append(order_data)

    return {"status": "ok", "orders": orders}

def save_payment_detail(payment_method, key, cardNumber=None, cardHolder=None, expiry=None, cvv=None, upiId=None):
    getSecretKey = SuperHelper.get_single_record("tbl_addresses", {"secret_key": key}, "*")
    if not getSecretKey:
        return {"status": "error", "message": "Secret key mismatch!"}
    payment_data = {
        "secret_key": key,
        "payment_method": payment_method,
    }
    if payment_method == "Card":
        if not all([cardNumber, cardHolder, expiry, cvv]):
            return {"status": "error", "message": "Incomplete Card details!"}
        payment_data = {
            "cardNumber": cardNumber,
            "cardHolder": cardHolder,
            "expiry": expiry,
            "cvv": cvv,
            "secret_key": key
        }
    elif payment_method == "UPI":
        if not upiId:
            return {"status": "error", "message": "UPI ID is required!"}
        payment_data = {
            "upiId": upiId,
             "secret_key": key
        }
    # print(payment_data)  # Debugging
    inserted_id = SuperHelper.add("tbl_payment_details", payment_data)

    return {"status": "success", "message": "Payment details saved successfully!"}

def generate_secret_key_for_order():
    prefix = "ORD_"
    while True:
        secret_key = prefix + secrets.token_hex(3)
        record = SuperHelper.get_single_record("tbl_addresses",{"secret_key": secret_key})
        if not record:
            return secret_key
        
def get_user_order_detail(request: Request, key):

    getSecretKey = SuperHelper.get_single_record(
        "tbl_addresses",
        {"secret_key": key},
        "*"
    )
    if not getSecretKey:
        return {"status": "error", "message": "Secret key Not Valid !"}

    users_products = SuperHelper.get_records(
        "tbl_orders",
        {"secret_key": key},
        "*"
    )
    
    # print(users_products)
    return {
        "status": "success",
        "data": users_products
    }
def Getoneproduct_details(request: Request,product_id):

    product = SuperHelper.get_single_record(
        "product",
        {"id": product_id},
        ["product_name", "product_image","price"]
    )
    if not product:
        return {"status": "error", "message": "Product not found"}

    return {
        "status": "success",
        "data": product
    }
def trackproduct_details(request: Request,id):

    product = SuperHelper.get_single_record(
        "tbl_orders",
        {"id": id},
        "*"
    )
    # if not product:
    #     return {"status": "error", "message": "Product not found"}
    print(product)
    return {
        "status": "success",
        "product": product
    }
def getaddress_details(request: Request,addressId):

    address = SuperHelper.get_single_record(
        "tbl_addresses",
        {"id": addressId},
        "*"
    )
    print(address)
    return {
        "status": "success",
        "address": address
    }
    

