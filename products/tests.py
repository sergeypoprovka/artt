from django.test import TestCase

from .models import Product


class TestProducts(TestCase):

    def test_can_create_product(self):
        product = Product.objects.create(client_id=1, title='Test Product', description='Test Description', price=1.00)
        self.assertEqual(product.client_id, 1)
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.price, 1.00)
        self.assertEqual(product.sale, False)
        self.assertEqual(product.in_stock, True)


class TestProductApi(TestCase):

    def test_can_fetch_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_can_fetch_single_product(self):
        product = Product.objects.create(client_id=1, title='Test Product', description='Test Description', price=1.00)
        response = self.client.get(f'/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Product')

    def test_can_update_product(self):
        product = Product.objects.create(client_id=1, title='Test Product', description='Test Description', price=1.00)
        response = self.client.patch(f'/products/{product.id}/', {'title': 'Updated'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated')
        product.refresh_from_db()
        self.assertEqual(product.title, 'Updated')

    def test_can_delete_product(self):
        product = Product.objects.create(client_id=1, title='Test Product', description='Test Description', price=1.00)
        response = self.client.delete(f'/products/{product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_can_set_sold_status(self):
        product = Product.objects.create(client_id=1, title='Test Product', description='Test Description', price=1.00)
        response = self.client.put(f'/products/{product.id}/sold/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Product sold successfully')
        product.refresh_from_db()
        self.assertEqual(product.in_stock, False)