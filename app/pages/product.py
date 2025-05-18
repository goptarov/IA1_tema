from flask import Blueprint, render_template, session, abort, current_app
import os, json

product_pages = Blueprint("product", __name__, url_prefix="/product")

def load_products():
    db_path = os.path.join(current_app.root_path, "../products.json")
    with open(db_path) as f:
        return json.load(f)

@product_pages.route("/<pid>")
def show_product(pid):
    products = load_products()
    product  = next((p for p in products if p["id"] == pid), None)
    if product is None:
        abort(404)

    cart_size = sum(session.get("cart", {}).values())
    return render_template(
        "product.html",
        product=product,
        cart_size=cart_size
    )
