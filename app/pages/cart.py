from flask import Blueprint, session, request, redirect, url_for, render_template
import os, json

cart_pages = Blueprint('cart', __name__)

def load_products():
    root = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(root, "../..", "products.json")
    with open(db_path, "r") as f:
        return json.load(f)

@cart_pages.route('/cart')
def show_cart():
    cart = session.get('cart', {})
    products = load_products()

    prod_by_id = { p['id']: p for p in products }

    items = []
    total = 0
    for pid, qty in cart.items():
        if pid not in prod_by_id:
            continue
        prod     = prod_by_id[pid]
        subtotal = prod['price'] * qty
        total   += subtotal
        items.append({
            'product':  prod,
            'quantity': qty,
            'subtotal': subtotal
        })

    return render_template('cart.html',
                           items=items,
                           total=total)

@cart_pages.route('/cart/add-item')
def add_item():
    pid = request.args.get('id')
    if not pid:
        return redirect(url_for('index.index_page'))

    cart = session.setdefault('cart', {})
    cart[pid] = cart.get(pid, 0) + 1
    session.modified = True

    # send them back to the product listing or the cart itself:
    return redirect(url_for('cart.show_cart'))

@cart_pages.route('/cart/remove-item')
def remove_item():
    pid = request.args.get('id')
    cart = session.get('cart', {})
    if pid in cart:
        cart.pop(pid)
        session.modified = True
    return redirect(url_for('cart.show_cart'))
