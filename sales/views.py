from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.views import CRUDListView
from sales.forms import CustomerForm
from sales.models import Customer, Sale


class CustomerListView(CRUDListView):
    model = Customer
    title = "Clientes"
    create_url = "customer-create"
    update_url_name = "customer-update"
    delete_url_name = "customer-delete"
    fields = ["name", "document_type", "document_number", "phone", "email", "is_generic"]
    field_labels = {
        "name": "Nombre",
        "document_type": "Tipo Doc.",
        "document_number": "Numero",
        "phone": "Telefono",
        "email": "Correo",
        "is_generic": "Generico",
    }


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("customer-list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente.")
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("customer-list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente.")
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = "crud/confirm_delete.html"
    success_url = reverse_lazy("customer-list")


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        return Sale.objects.select_related("branch", "warehouse", "customer", "seller").order_by("-created_at")[:100]
