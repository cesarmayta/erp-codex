from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import Branch, Sequence, TimeStampedModel, Warehouse


class Customer(TimeStampedModel):
    class DocumentType(models.TextChoices):
        DNI = "DNI", "DNI"
        RUC = "RUC", "RUC"
        CE = "CE", "Carnet de extranjeria"

    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=10, choices=DocumentType.choices, blank=True)
    document_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_generic = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Sale(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="sales")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="sales")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="sales")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="sales")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    document_number = models.CharField(max_length=24, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    notes = models.CharField(max_length=255, blank=True)

    def assign_document_number(self) -> None:
        if self.document_number:
            return
        sequence, _created = Sequence.objects.get_or_create(
            branch=self.branch,
            document_type="sale",
            prefix=self.branch.series_prefix,
        )
        self.document_number = sequence.consume()


class SaleLine(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, related_name="sale_lines")
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))


class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        MIXED = "mixed", "Mixed"

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=20, choices=Method.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True)
