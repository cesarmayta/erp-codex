from rest_framework import serializers

from inventory.models import Category, Product, StockMovement, StockSnapshot


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class StockSnapshotSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)

    class Meta:
        model = StockSnapshot
        fields = "__all__"


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = "__all__"
