from django import forms

from core.forms import BootstrapFormMixin
from inventory.models import Category, Product, StockMovement


class CategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class ProductForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "sku",
            "name",
            "category",
            "unit",
            "cost_price",
            "sale_price",
            "low_stock_threshold",
            "is_active",
        ]


class StockMovementForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ["movement_type", "product", "warehouse", "quantity", "reference", "notes"]
