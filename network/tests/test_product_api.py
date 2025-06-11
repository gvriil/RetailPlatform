from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from network.models import Product, NetworkNode
from datetime import date


class ProductAPITests(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        # Set up API client
        self.node1 = NetworkNode.objects.create(
            name="Node 1",
            email="node1@example.com",
            country="Country1",
            city="City1",
            street="Street1",
            house_number="10",
            node_type="factory",
        )
        self.node2 = NetworkNode.objects.create(
            name="Node 2",
            email="node2@example.com",
            country="Country2",
            city="City2",
            street="Street2",
            house_number="20",
            node_type="factory",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.factory_node = NetworkNode.objects.create(
            name="Test Factory",
            email="factory@example.com",
            country="Test Country",
            city="Test City",
            street="Test Street",
            house_number="1",
            node_type="factory",
        )

        self.product = Product.objects.create(
            name="Test Product",
            model="Test Model",
            release_date=date.today(),
            price=100.00,
            quantity=10,
        )
        self.product.nodes.add(self.factory_node)

        # API URLs
        self.products_url = reverse("product-list")
        self.product_detail_url = reverse("product-detail",
                                          args=[self.product.id])

    def test_get_products(self):
        """Test retrieving all products"""
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Product")

    def test_get_product_detail(self):
        """Test retrieving a single product"""
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Product")
        self.assertEqual(response.data["model"], "Test Model")

    def test_create_product(self):
        # Get initial count
        initial_count = Product.objects.count()

        # Your test data and request
        data = {
            "name": "Test Product",
            "model": "TP-100",
            "release_date": "2024-01-01",
            "price": "0.00",
            "quantity": 0,
            "nodes": [self.node1.id, self.node2.id],
        }
        response = self.client.post(self.products_url, data, format="json")

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check one product was added
        self.assertEqual(Product.objects.count(), initial_count + 1)

    def test_update_product(self):
        """Test updating an existing product"""
        data = {
            "name": "Updated Product",
            "model": "Test Model",
            "release_date": date.today().isoformat(),
            "price": 150.00,
            "quantity": 10,
            "nodes": [self.factory_node.id],
        }
        response = self.client.put(self.product_detail_url, data,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")
        self.assertEqual(self.product.price, 150.00)

    def test_delete_product(self):
        """Test deleting a product"""
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
