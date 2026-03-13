from decimal import Decimal

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Branch(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    series_prefix = models.CharField(max_length=10, default="B001")

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Warehouse(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="warehouses")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Sequence(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="sequences")
    document_type = models.CharField(max_length=32)
    prefix = models.CharField(max_length=10)
    next_number = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("branch", "document_type", "prefix")

    def consume(self) -> str:
        number = self.next_number
        self.next_number += 1
        self.save(update_fields=["next_number", "updated_at"])
        return f"{self.prefix}-{number:08d}"


class AuditLog(TimeStampedModel):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]


class BusinessSetting(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)

    @classmethod
    def get_decimal(cls, key: str, default: Decimal) -> Decimal:
        setting = cls.objects.filter(key=key).first()
        return Decimal(setting.value) if setting else default


class Company(TimeStampedModel):
    business_name = models.CharField(max_length=255)
    trade_name = models.CharField(max_length=255, blank=True)
    ruc = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    currency_code = models.CharField(max_length=3, default="PEN")
    timezone = models.CharField(max_length=64, default="America/Lima")

    def __str__(self) -> str:
        return self.trade_name or self.business_name
