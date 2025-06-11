# network/serializers.py
from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Handles the serialization and deserialization of Product objects,
    including their relationships with NetworkNode objects.
    """

    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date",
                  "price", "quantity", "nodes"]

    def to_representation(self, instance):
        """
        Custom representation of Product model.

        Overrides the default representation to format nodes as a list of
        objects with id and name rather than just IDs.

        Args:
            instance: The Product instance being serialized

        Returns:
            dict: The serialized representation of the Product
        """
        representation = super().to_representation(instance)
        representation["nodes"] = [
            {"id": node.id, "name": node.name} for node in instance.nodes.all()
        ]
        return representation


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Basic serializer for NetworkNode model.

    Used for list operations with essential fields, while the detail
    serializer provides expanded relationship data.
    """

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "city",
            "country",
            "node_type",
            "supplier",
            "debt",
            "level",
            "created_at",
        ]


class NetworkNodeDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for NetworkNode with expanded relationship data.
    Used for retrieve operations to provide more comprehensive information.
    """

    supplier_details = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "city",
            "country",
            "node_type",
            "supplier",
            "supplier_details",
            "debt",
            "level",
            "created_at",
            "products",
        ]

    def get_supplier_details(self, obj):
        """Return expanded supplier information if available"""
        if obj.supplier:
            return {
                "id": obj.supplier.id,
                "name": obj.supplier.name,
                "city": obj.supplier.city,
            }
        return None

    def get_products(self, obj):
        """Return all products associated with this node"""
        products = obj.product_set.all()
        return ProductSerializer(products, many=True).data
