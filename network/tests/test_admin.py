from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from network.admin import NetworkNodeAdmin
from network.models import NetworkNode


class AdminActionsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = AdminSite()
        self.admin = NetworkNodeAdmin(NetworkNode, self.admin_site)

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

        self.retail_node = NetworkNode.objects.create(
            name="Test Retail",
            email="retail@example.com",
            country="Test Country",
            city="Test City",
            street="Test Street",
            house_number="2",
            node_type="retail",
            supplier=self.factory_node,
            debt=1000,
        )

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

    def test_clear_debt_action(self):
        """Test admin action for clearing debt."""
        # Set up request and messages
        request = self.factory.get("/")
        request.user = self.admin_user

        # Set up messaging framework
        setattr(request, "session", "session")
        setattr(request, "_messages", FallbackStorage(request))

        # Test the clear_debt action
        queryset = NetworkNode.objects.filter(pk=self.retail_node.pk)
        self.assertEqual(self.retail_node.debt, 1000)
        self.admin.clear_debt(request, queryset)

        # Refresh from database and check debt is cleared
        self.retail_node.refresh_from_db()
        self.assertEqual(self.retail_node.debt, 0)
