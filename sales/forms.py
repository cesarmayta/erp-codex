from django import forms

from core.forms import BootstrapFormMixin
from sales.models import Customer


class CustomerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "document_type", "document_number", "email", "phone", "is_generic"]
