"""
Network application configuration module.

This module defines the Django app configuration for the network application,
which handles the retail platform's network management, including nodes,
products, and their relationships.
"""

from django.apps import AppConfig


class NetworkConfig(AppConfig):
    """
    Configuration class for the network application.

    This class defines settings for the network app, which is responsible
    for managing the retail platform's distribution network, including
    retail nodes, products, and inventory management.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "network"
