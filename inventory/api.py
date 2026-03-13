from decimal import Decimal

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from inventory.models import Category, Product, StockMovement, StockSnapshot
from inventory.serializers import CategorySerializer, ProductSerializer, StockMovementSerializer, StockSnapshotSerializer
from inventory.services import register_stock_movement
from core.models import Warehouse


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ["name"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    search_fields = ["sku", "name"]
    ordering_fields = ["sku", "name", "sale_price"]


class StockSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockSnapshot.objects.select_related("product", "warehouse").all()
    serializer_class = StockSnapshotSerializer
    filterset_fields = ["warehouse", "product"]


class StockMovementViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = StockMovement.objects.select_related("product", "warehouse").all()
    serializer_class = StockMovementSerializer
    filterset_fields = ["movement_type", "warehouse", "product"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=serializer.validated_data["product"].id)
        warehouse = Warehouse.objects.get(pk=serializer.validated_data["warehouse"].id)
        movement = register_stock_movement(
            movement_type=serializer.validated_data["movement_type"],
            product=product,
            warehouse=warehouse,
            quantity=Decimal(serializer.validated_data["quantity"]),
            reference=serializer.validated_data.get("reference", ""),
            notes=serializer.validated_data.get("notes", ""),
            actor=request.user,
        )
        return Response(self.get_serializer(movement).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        queryset = StockSnapshot.objects.select_related("product", "warehouse").all()
        items = [item for item in queryset if item.quantity <= item.product.low_stock_threshold]
        return Response(StockSnapshotSerializer(items, many=True).data)
