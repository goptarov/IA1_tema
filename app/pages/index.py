from flask import session, Blueprint, request, redirect, render_template
import json, os


index_pages = Blueprint("index", __name__)

def load_products():
    root = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(root, "../..", "products.json")
    with open(db_path, "r") as f:
        return json.load(f)

@index_pages.route("/")
def index_page():
    if not session.get("auth", False):
        return redirect("/login", code=302)
    products = load_products()
    cart_size = sum(session.get("cart", {}).values())
    return render_template("index.html",
                           products=products,
                           cart_size=cart_size)

@index_pages.route("/contact")
def contact_page():
    return render_template("contact.html")
