from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(255))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}
