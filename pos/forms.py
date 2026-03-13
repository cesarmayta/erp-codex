from django import forms

from cash.models import CashSession
from core.forms import BootstrapFormMixin
from core.models import Branch, Warehouse
from sales.models import Customer, Payment


class POSCheckoutForm(BootstrapFormMixin, forms.Form):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all())
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.select_related("branch").all())
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    cash_session = forms.ModelChoiceField(queryset=CashSession.objects.filter(status=CashSession.Status.OPEN))
    payment_method = forms.ChoiceField(choices=Payment.Method.choices)
    receipt_type = forms.ChoiceField(
        choices=[("ticket", "Ticket interno"), ("boleta", "Boleta interna"), ("factura", "Factura interna")],
        initial="ticket",
    )
    received_amount = forms.DecimalField(decimal_places=2, max_digits=12, required=False)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
