import unittest
from app import app, db, Product, Cart

class EcommerceTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            db.session.add(Product(name="TestProduct", price=99.99, image_url="https://example.com/test.jpg"))
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestProduct', response.data)

    def test_add_to_cart(self):
        with app.app_context():
            product = Product.query.first()
        response = self.client.post('/cart', json={'id': product.id})
        self.assertEqual(response.status_code, 200)
        cart_response = self.client.get('/cart')
        self.assertIn(b'TestProduct', cart_response.data)

    def test_cart_clear(self):
        with app.app_context():
            product = Product.query.first()
        self.client.post('/cart', json={'id': product.id})
        response = self.client.delete('/cart')
        self.assertEqual(response.status_code, 200)
        cart_response = self.client.get('/cart')
        self.assertNotIn(b'TestProduct', cart_response.data)

if __name__ == '__main__':
    unittest.main()
