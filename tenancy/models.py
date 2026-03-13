from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


class Client(TenantMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=2, default="PE")
    currency_code = models.CharField(max_length=3, default="PEN")
    timezone = models.CharField(max_length=64, default="America/Lima")

    auto_create_schema = True

    def __str__(self) -> str:
        return self.name


class Domain(DomainMixin):
    pass
