# network/tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from network.models import NetworkNode, Product
from decimal import Decimal
from datetime import date


class NetworkNodeModelTests(TestCase):
    """Tests for the NetworkNode model."""

    def setUp(self):
        """Set up test data."""
        # Create a factory (top level)
        self.factory = NetworkNode.objects.create(
            name="Test Factory",
            email="factory@example.com",
            country="Test Country",
            city="Test City",
            street="Factory Street",
            house_number="1",
            node_type="factory",
        )

        # Create a retail node (level 1)
        self.retail = NetworkNode.objects.create(
            name="Test Retail",
            email="retail@example.com",
            country="Test Country",
            city="Test City",
            street="Retail Street",
            house_number="2",
            node_type="retail",
            supplier=self.factory,
        )

        # Create an entrepreneur node (level 2)
        self.entrepreneur = NetworkNode.objects.create(
            name="Test Entrepreneur",
            email="entrepreneur@example.com",
            country="Test Country",
            city="Test City",
            street="Entrepreneur Street",
            house_number="3",
            node_type="entrepreneur",
            supplier=self.retail,
        )

    def test_hierarchy_levels(self):
        """Test that hierarchy levels are calculated correctly."""
        self.assertEqual(self.factory.level, 0)
        self.assertEqual(self.retail.level, 1)
        self.assertEqual(self.entrepreneur.level, 2)

    def test_factory_cannot_have_supplier(self):
        """Test that a factory cannot have a supplier."""
        invalid_factory = NetworkNode(
            name="Invalid Factory",
            email="invalid@example.com",
            country="Test Country",
            city="Test City",
            street="Invalid Street",
            house_number="4",
            node_type="factory",
            supplier=self.retail,
        )

        with self.assertRaises(ValidationError):
            invalid_factory.full_clean()

    def test_circular_reference_prevention(self):
        """Test that circular references are prevented."""
        # Try to make the factory have the entrepreneur as supplier
        self.factory.supplier = self.entrepreneur

        with self.assertRaises(ValidationError):
            self.factory.full_clean()

    def test_string_representation(self):
        """Test the string representation of the model."""
        self.assertEqual(str(self.factory), "Test Factory")

    def test_update_client_levels(self):
        """Test that updating a node updates the levels of its clients."""
        # Create a new supplier for the retail node
        new_factory = NetworkNode.objects.create(
            name="New Factory",
            email="new@example.com",
            country="Test Country",
            city="Test City",
            street="New Street",
            house_number="5",
            node_type="factory",
        )

        # Change the retail's supplier
        self.retail.supplier = new_factory
        self.retail.save()

        # Refresh the entrepreneur from the database
        self.entrepreneur.refresh_from_db()

        # Check that the entrepreneur's level is still 2
        self.assertEqual(self.entrepreneur.level, 2)


class ProductModelTests(TestCase):
    """Tests for the Product model."""

    def setUp(self):
        """Set up test data."""
        self.node = NetworkNode.objects.create(
            name="Test Node",
            email="node@example.com",
            country="Test Country",
            city="Test City",
            street="Node Street",
            house_number="1",
            node_type="retail",
        )

        self.product = Product.objects.create(
            name="Test Product",
            model="Test Model",
            release_date=date.today(),
            price=Decimal("99.99"),
            quantity=10,
        )
        self.product.nodes.add(self.node)

    def test_string_representation(self):
        """Test the string representation of the model."""
        self.assertEqual(str(self.product), "Test Product - Test Model")

    def test_product_node_relationship(self):
        """Test the many-to-many relationship between products and nodes."""
        self.assertEqual(self.product.nodes.count(), 1)
        self.assertEqual(self.product.nodes.first(), self.node)

        # Check the reverse relationship
        self.assertEqual(self.node.products.count(), 1)
        self.assertEqual(self.node.products.first(), self.product)
