from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from cash.models import CashSession
from core.forms import BranchForm, BusinessSettingForm, CompanyForm, WarehouseForm
from core.models import Branch, BusinessSetting, Company, Warehouse
from inventory.models import Product, StockSnapshot
from sales.models import Sale


class CRUDListView(LoginRequiredMixin, ListView):
    template_name = "crud/list.html"
    context_object_name = "objects"
    title = ""
    create_url = ""
    update_url_name = ""
    delete_url_name = ""
    fields = []
    field_labels = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title,
                "create_url": self.create_url,
                "update_url_name": self.update_url_name,
                "delete_url_name": self.delete_url_name,
                "fields": self.fields,
                "field_labels": self.field_labels,
            }
        )
        return context


class CRUDCreateView(LoginRequiredMixin, CreateView):
    template_name = "crud/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = getattr(self, "title", self.model._meta.verbose_name.title())
        return context

    def form_valid(self, form):
        messages.success(self.request, "Registro creado correctamente.")
        return super().form_valid(form)


class CRUDUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "crud/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = getattr(self, "title", self.model._meta.verbose_name.title())
        return context

    def form_valid(self, form):
        messages.success(self.request, "Registro actualizado correctamente.")
        return super().form_valid(form)


class CRUDDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "crud/confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = getattr(self, "title", self.model._meta.verbose_name.title())
        return context

    def form_valid(self, form):
        messages.success(self.request, "Registro eliminado correctamente.")
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_count"] = Product.objects.count()
        context["sale_count"] = Sale.objects.count()
        context["open_sessions"] = CashSession.objects.filter(status=CashSession.Status.OPEN).count()
        context["low_stock"] = [
            snapshot for snapshot in StockSnapshot.objects.select_related("product", "warehouse")
            if snapshot.quantity <= snapshot.product.low_stock_threshold
        ][:5]
        return context


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("company-edit")

    def get_object(self, queryset=None):
        company, _created = Company.objects.get_or_create(
            pk=1,
            defaults={"business_name": "Empresa 1 SAC", "trade_name": "Empresa 1"},
        )
        return company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Empresa"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Datos de la empresa actualizados.")
        return super().form_valid(form)


class BranchListView(CRUDListView):
    model = Branch
    title = "Sucursales"
    create_url = "branch-create"
    update_url_name = "branch-update"
    delete_url_name = "branch-delete"
    fields = ["code", "name", "address", "series_prefix", "is_active"]
    field_labels = {
        "code": "Codigo",
        "name": "Nombre",
        "address": "Direccion",
        "series_prefix": "Serie",
        "is_active": "Activo",
    }


class BranchCreateView(CRUDCreateView):
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy("branch-list")
    title = "Nueva sucursal"


class BranchUpdateView(CRUDUpdateView):
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy("branch-list")
    title = "Editar sucursal"


class BranchDeleteView(CRUDDeleteView):
    model = Branch
    success_url = reverse_lazy("branch-list")
    title = "Eliminar sucursal"


class WarehouseListView(CRUDListView):
    model = Warehouse
    title = "Almacenes"
    create_url = "warehouse-create"
    update_url_name = "warehouse-update"
    delete_url_name = "warehouse-delete"
    fields = ["code", "name", "branch", "is_active"]
    field_labels = {"code": "Codigo", "name": "Nombre", "branch": "Sucursal", "is_active": "Activo"}


class WarehouseCreateView(CRUDCreateView):
    model = Warehouse
    form_class = WarehouseForm
    success_url = reverse_lazy("warehouse-list")
    title = "Nuevo almacen"


class WarehouseUpdateView(CRUDUpdateView):
    model = Warehouse
    form_class = WarehouseForm
    success_url = reverse_lazy("warehouse-list")
    title = "Editar almacen"


class WarehouseDeleteView(CRUDDeleteView):
    model = Warehouse
    success_url = reverse_lazy("warehouse-list")
    title = "Eliminar almacen"


class BusinessSettingListView(CRUDListView):
    model = BusinessSetting
    title = "Parametros del negocio"
    create_url = "setting-create"
    update_url_name = "setting-update"
    delete_url_name = "setting-delete"
    fields = ["key", "value"]
    field_labels = {"key": "Clave", "value": "Valor"}


class BusinessSettingCreateView(CRUDCreateView):
    model = BusinessSetting
    form_class = BusinessSettingForm
    success_url = reverse_lazy("setting-list")
    title = "Nuevo parametro"


class BusinessSettingUpdateView(CRUDUpdateView):
    model = BusinessSetting
    form_class = BusinessSettingForm
    success_url = reverse_lazy("setting-list")
    title = "Editar parametro"


class BusinessSettingDeleteView(CRUDDeleteView):
    model = BusinessSetting
    success_url = reverse_lazy("setting-list")
    title = "Eliminar parametro"
