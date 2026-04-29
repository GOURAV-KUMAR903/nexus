# ==========================================================
# 1️⃣ Table ke saare records fetch karna
# ==========================================================

all_products = SuperHelper.get_records("product")


# ==========================================================
# 2️⃣ WHERE condition ke saath records fetch karna
# ==========================================================

# secret_key = "ABC123"

products = SuperHelper.get_records(
    "product",
    {"secret_key": "ABC123"}
)


# ==========================================================
# 3️⃣ Specific columns fetch karna
# ==========================================================

products = SuperHelper.get_records(
    "product",
    None,
    ["id", "product_name", "price"]
)


# ==========================================================
# 4️⃣ WHERE + Specific columns
# ==========================================================

products = SuperHelper.get_records(
    "product",
    {"secret_key": "ABC123"},
    ["id", "product_name", "price"]
)


# ==========================================================
# 5️⃣ Multiple WHERE conditions
# ==========================================================

products = SuperHelper.get_records(
    "product",
    {
        "secret_key": "ABC123",
        "status": "active"
    }
)


# ==========================================================
# 6️⃣ Ek column bhi fetch kar sakte ho
# ==========================================================

products = SuperHelper.get_records(
    "product",
    None,
    ["product_name"]
)


# ==========================================================
# 7️⃣ Controller / Service me use
# ==========================================================

def product_page(request: Request):

    # product table ke saare records
    all_products = SuperHelper.get_records("product")

    products_json = json.dumps(jsonable_encoder(all_products))

    return render_view(
        "product_details.html",
        request,
        {
            "title": "Product Details",
            "products_json": products_json,
            "base_url": BASE_URL,
            "CURRENCY": CURRENCY
        }
    )