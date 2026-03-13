from django import forms

from core.models import Branch, BusinessSetting, Company, Warehouse


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select"
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = "form-control"
            else:
                widget.attrs["class"] = "form-control"


class CompanyForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Company
        fields = ["business_name", "trade_name", "ruc", "address", "phone", "email", "currency_code", "timezone"]


class BranchForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["code", "name", "address", "series_prefix", "is_active"]


class WarehouseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["code", "name", "branch", "is_active"]


class BusinessSettingForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = BusinessSetting
        fields = ["key", "value"]
