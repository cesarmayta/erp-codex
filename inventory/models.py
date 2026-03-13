from decimal import Decimal

from django.db import models

from core.models import TimeStampedModel, Warehouse


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="products")
    unit = models.CharField(max_length=20, default="NIU")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    is_active = models.BooleanField(default=True)
    low_stock_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"


class StockSnapshot(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="snapshots")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stock_snapshots")
    quantity = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        unique_together = ("product", "warehouse")


class StockMovement(TimeStampedModel):
    class MovementType(models.TextChoices):
        IN = "in", "Ingreso"
        OUT = "out", "Salida"
        ADJUSTMENT = "adjustment", "Ajuste"
        TRANSFER = "transfer", "Transferencia"

    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_movements")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="stock_movements")
    reference = models.CharField(max_length=100, blank=True)
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
