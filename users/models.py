from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        CASHIER = "cashier", "Cashier"
        SELLER = "seller", "Seller"
        WAREHOUSE = "warehouse", "Warehouse"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)
    branch_code = models.CharField(max_length=32, blank=True)

    @property
    def can_discount(self) -> bool:
        return self.role in {self.Role.OWNER, self.Role.ADMIN, self.Role.SELLER}
