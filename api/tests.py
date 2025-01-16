# Create your tests here.
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.exceptions import InvaidSchemaException
from api.models import Product, Order
from api.dataclasses import ProductData


class ProductTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product", description="A sample product", price=10.0, stock=50
        )

    def test_get_products(self):
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json()[0])

    def test_create_product(self):
        data = {
            "name": "New Product",
            "description": "A new sample product",
            "price": 20.0,
            "stock": 100,
        }
        response = self.client.post(
            reverse("product-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_invalid_data(self):
        data = {"name": "", "description": "", "price": -5, "stock": -10}
        response = self.client.post(
            reverse("product-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Order Product",
            description="Product for order test",
            price=15.0,
            stock=30,
        )

    def test_create_order_success(self):
        data = {"products": [{"id": self.product.id, "quantity": 5}]}
        response = self.client.post(
            reverse("order-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 25)

    def test_create_order_insufficient_stock(self):
        data = {"products": [{"id": self.product.id, "quantity": 35}]}
        response = self.client.post(
            reverse("order-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Some of the products are out of stock..", response.json()["detail"]
        )

    def test_create_order_product_does_not_exist(self):
        data = {"products": [{"id": 9999, "quantity": 1}]}
        response = self.client.post(
            reverse("order-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Product with id = 9999 does not exist", response.json()["detail"]
        )

    def test_create_order_invalid_schema(self):
        data = {"products": [{"id": self.product.id}]}
        response = self.client.post(
            reverse("order-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid product schema..", response.json()["detail"])


class ProductDataTests(APITestCase):
    def test_product_data_from_json_success(self):
        data = {"id": 1, "quantity": 10}
        product_data = ProductData.from_json(data)
        self.assertEqual(product_data.id, 1)
        self.assertEqual(product_data.quantity, 10)

    def test_product_data_from_json_invalid_schema(self):
        data = {"id": 1}
        with self.assertRaises(InvaidSchemaException):
            ProductData.from_json(data)
