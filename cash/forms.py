from django import forms

from cash.models import CashEntry, CashRegister
from core.forms import BootstrapFormMixin


class CashRegisterForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CashRegister
        fields = ["branch", "code", "name", "is_active"]


class CashOpenForm(BootstrapFormMixin, forms.Form):
    cash_register = forms.ModelChoiceField(queryset=CashRegister.objects.filter(is_active=True))
    opening_amount = forms.DecimalField(decimal_places=2, max_digits=12)


class CashCloseForm(BootstrapFormMixin, forms.Form):
    closing_amount = forms.DecimalField(decimal_places=2, max_digits=12)


class CashEntryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CashEntry
        fields = ["session", "entry_type", "amount", "description"]
