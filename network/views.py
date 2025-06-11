# network/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from .models import NetworkNode, Product
from .serializers import (
    NetworkNodeSerializer,
    ProductSerializer,
    NetworkNodeDetailSerializer,
)
from .pagination import StandardResultsSetPagination


class IsActiveEmployee(permissions.BasePermission):
    """Custom permission to allow only active employees."""

    def has_permission(self, request, view):
        return (request.user and
                request.user.is_authenticated and
                request.user.is_active)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for NetworkNode model providing CRUD operations.
    Prevents updating the debt field via API.
    """

    queryset = NetworkNode.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["country", "city", "node_type"]
    search_fields = ["name", "email"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NetworkNodeDetailSerializer
        return NetworkNodeSerializer

    def perform_update(self, serializer):
        """Prevent updating debt field through API"""
        instance = self.get_object()
        serializer.save(debt=instance.debt)

    @action(detail=True, methods=["post"])
    def clear_debt(self, request, pk=None):
        """Custom endpoint to clear debt for a specific node"""
        node = self.get_object()
        node.debt = 0
        node.save()
        return Response({"status": "debt cleared"})

    @action(detail=False)
    def statistics(self, request):
        """Aggregated statistics about network nodes"""
        stats = {
            "total_nodes": NetworkNode.objects.count(),
            "total_debt":
                NetworkNode.objects.aggregate(Sum("debt"))["debt__sum"] or 0,
            "nodes_by_level": dict(
                NetworkNode.objects.values("level")
                .annotate(count=Count("id"))
                .values_list("level", "count")
            ),
            "nodes_by_country": dict(
                NetworkNode.objects.values("country")
                .annotate(count=Count("id"))
                .values_list("country", "count")
            ),
        }
        return Response(stats)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for product management.
    Provides standard CRUD operations with filtering and ordering.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["release_date", "model"]
    search_fields = ["name", "model"]
    ordering_fields = ["price", "release_date", "name"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optimize queries with prefetch_related for the nodes M2M relationship
        """
        return Product.objects.prefetch_related("nodes").all()
