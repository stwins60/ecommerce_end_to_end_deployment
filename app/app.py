
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from models import db, Product, Cart
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
from dotenv import load_dotenv
import sqlite3


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
app = Flask(__name__)

# Use SQLite for local development/testing
if os.getenv('FLASK_ENV', 'production') == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

db.init_app(app)


# Add Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info("app_info", "E-commerce Flask App with Prometheus", version="1.0.0")


# Define custom metrics once
cart_size_gauge = Gauge("cart_size", "Number of items in shopping cart")


def create_tables():
    db.create_all()
    if not Product.query.first():
        db.session.add_all([
            Product(name="Laptop", price=1200, image_url="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80"),
            Product(name="Phone", price=800, image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=400&q=80"),
            Product(name="Headphones", price=150, image_url="https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=400&q=80")
        ])
        db.session.commit()




# Landing page
@metrics.do_not_track()
@app.route("/landing")
def landing():
    return render_template("landing.html")


# health check
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

# Product listing
@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)



# Product details
@app.route("/product/<int:product_id>")
def product_page(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product)



# Cart page
@app.route("/cart-page")
def cart_page():
    return render_template("cart.html")



# Checkout page
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        # Here you would process the order, payment, etc.
        # For demo, just clear the cart
        Cart.query.delete()
        db.session.commit()
        return jsonify({"status": "success"})
    return render_template("checkout.html")


# Cart API
@app.route("/cart", methods=["POST", "GET", "DELETE"])
def cart():
    if request.method == "POST":
        product_id = request.json.get("id")
        product = Product.query.get(product_id)
        if product:
            new_item = Cart(product_id=product.id, name=product.name, price=product.price)
            db.session.add(new_item)
            db.session.commit()
    elif request.method == "DELETE":
        data = request.get_json(silent=True)
        if data and "id" in data:
            item = Cart.query.get(data["id"])
            if item:
                db.session.delete(item)
                db.session.commit()
        else:
            Cart.query.delete()
            db.session.commit()
        items = Cart.query.all()
        cart_size_gauge.set(len(items))
        return jsonify([c.to_dict() for c in items])
    items = Cart.query.all()
    cart_size_gauge.set(len(items))  # update metric
    return jsonify([c.to_dict() for c in items])


# Serve static files for CSS and JS
@app.route('/templates/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates'), filename)


if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(host="0.0.0.0", port=5000)
