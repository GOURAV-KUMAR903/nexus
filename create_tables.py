# create_tables.py
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData ,Float
from database.db import Base, engine
from models.product_model import Product  # Product model import

# Step 1: Create tables defined in Base (like Product)
Base.metadata.create_all(bind=engine)

# Step 2: Create tbl_addresses manually (without model)
metadata = MetaData()

tbl_addresses = Table(
    "tbl_addresses",  # Table name
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("address", String(500), nullable=False),
    Column("city", String(100), nullable=False),
    Column("zip", String(20), nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)
tbl_orders = Table(
    "tbl_orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("secret_key", String(255), nullable=False),
    Column("order_id", Integer, nullable=False),
    Column("address_id", Integer, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("price", Float, nullable=False),
    Column("payment_method", String(50), nullable=False),
    Column("status", String(50), default="Pending"),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)
tbl_payment_details = Table(
    "tbl_payment_details",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("secret_key", String(255), nullable=False),  # link with order/address
    Column("cardNumber", String(20), nullable=True),    # optional if UPI
    Column("cardHolder", String(255), nullable=True),
    Column("expiry", String(10), nullable=True),
    Column("cvv", String(10), nullable=True),
    Column("upiId", String(100), nullable=True),        # optional if card
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)
# Step 3: Create the table in DB
metadata.create_all(engine)

print("Tables created successfully!")