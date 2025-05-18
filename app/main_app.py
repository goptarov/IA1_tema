# Imported symbols here please!
from flask import Flask, request, render_template, redirect, session
from .pages.index import index_pages
from .pages.auth import auth_pages
from .pages.cart import cart_pages
from .pages.checkout import checkout_pages
from .pages.product import product_pages
# Initialize the Flask application
# Note: static folder means all files in there will be automatically offered over HTTP
app = Flask(__name__, static_folder="../public",
            template_folder="../templates")
app.secret_key = "gxnMaYjinQ27DeBwgKsDyuDQO"
app.register_blueprint(index_pages)
app.register_blueprint(auth_pages)
app.register_blueprint(cart_pages)
app.register_blueprint(checkout_pages)
app.register_blueprint(product_pages)