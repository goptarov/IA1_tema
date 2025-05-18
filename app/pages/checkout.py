from flask import Blueprint, session, request, render_template, redirect, url_for, current_app
import os, json
from datetime import datetime

checkout_pages = Blueprint('checkout', __name__)

def load_products():
    root = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(root, "../..", "products.json")
    with open(db_path, "r") as f:
        return json.load(f)

def save_order(order):
    orders_path = os.path.join(current_app.root_path, '../orders.json')
    if not os.path.exists(orders_path):
        f = open(orders_path, 'w')
        json.dump([], f, indent=2)

    f = open(orders_path, 'r+')
    data = json.load(f)
    data.append(order)
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()

@checkout_pages.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    products = load_products()
    prod_by_id = {p['id']: p for p in products}


    items = []
    total = 0.0
    for pid, qty in cart.items():
        prod = prod_by_id.get(pid)
        if not prod:
            continue
        subtotal = prod['price'] * qty
        items.append({
            'product':  prod,
            'quantity': qty,
            'subtotal': subtotal
        })
        total += subtotal

    if request.method == 'GET':

        return render_template('checkout.html',
                               items=items,
                               total=total,
                               form = {},
                               error = None)


    full_name = request.form.get('full_name', '').strip()
    email     = request.form.get('email', '').strip()
    address   = request.form.get('address', '').strip()
    city      = request.form.get('city', '').strip()
    zip_code  = request.form.get('zip_code', '').strip()

    if not (full_name and email and address and city and zip_code):
        error = "All fields are required."
        return render_template('checkout.html',
                               items=items,
                               total=total,
                               error=error,
                               form=request.form)
    order = {
        'timestamp':  datetime.utcnow().isoformat() + 'Z',
        'full_name':  full_name,
        'email':      email,
        'address':    address,
        'city':       city,
        'zip_code':   zip_code,
        'items':      { pid: qty for pid, qty in cart.items() },
        'total':      total
    }

    # Persist to disk
    save_order(order)

    # Clear cart
    session.pop('cart', None)

    items = []

    for pid, qty in order['items'].items():
        prod = prod_by_id.get(pid)
        if not prod:
            continue
        items.append({'product': prod, 'quantity': qty, 'subtotal': prod['price'] * qty})

      # Show thank-you page, passing both order metadata and resolved items

    return render_template('thank_you.html', order=order, items = items)
