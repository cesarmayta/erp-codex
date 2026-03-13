from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView
from django.db.models import Q

from core.views import CRUDListView
from inventory.forms import CategoryForm, ProductForm, StockMovementForm
from inventory.models import Category, Product, StockMovement, StockSnapshot
from inventory.services import register_stock_movement


class CategoryListView(CRUDListView):
    model = Category
    title = "Categorias"
    create_url = "category-create"
    update_url_name = "category-update"
    delete_url_name = "category-delete"
    fields = ["name"]
    field_labels = {"name": "Nombre"}


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("category-list")
    extra_context = {"title": "Nueva categoria"}

    def form_valid(self, form):
        messages.success(self.request, "Categoria creada correctamente.")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("category-list")
    extra_context = {"title": "Editar categoria"}

    def form_valid(self, form):
        messages.success(self.request, "Categoria actualizada correctamente.")
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "crud/confirm_delete.html"
    success_url = reverse_lazy("category-list")
    extra_context = {"title": "Eliminar categoria"}


class ProductListView(CRUDListView):
    model = Product
    title = "Productos"
    create_url = "product-create"
    update_url_name = "product-update"
    delete_url_name = "product-delete"
    fields = ["sku", "name", "category", "sale_price", "low_stock_threshold", "is_active"]
    field_labels = {
        "sku": "SKU",
        "name": "Nombre",
        "category": "Categoria",
        "sale_price": "Precio",
        "low_stock_threshold": "Stock minimo",
        "is_active": "Activo",
    }


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("product-list")
    extra_context = {"title": "Nuevo producto"}

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("product-list")
    extra_context = {"title": "Editar producto"}

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "crud/confirm_delete.html"
    success_url = reverse_lazy("product-list")
    extra_context = {"title": "Eliminar producto"}


class StockSnapshotListView(LoginRequiredMixin, ListView):
    model = StockSnapshot
    template_name = "inventory/snapshot_list.html"
    context_object_name = "snapshots"

    def get_queryset(self):
        return StockSnapshot.objects.select_related("product", "warehouse", "warehouse__branch").order_by("product__name")


class StockMovementListView(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = "inventory/movement_list.html"
    context_object_name = "movements"

    def get_queryset(self):
        return StockMovement.objects.select_related("product", "warehouse").order_by("-created_at")[:100]


class StockMovementCreateView(LoginRequiredMixin, FormView):
    form_class = StockMovementForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("stock-movement-list")
    extra_context = {"title": "Nuevo movimiento de stock"}

    def form_valid(self, form):
        register_stock_movement(
            movement_type=form.cleaned_data["movement_type"],
            product=form.cleaned_data["product"],
            warehouse=form.cleaned_data["warehouse"],
            quantity=form.cleaned_data["quantity"],
            reference=form.cleaned_data["reference"],
            notes=form.cleaned_data["notes"],
            actor=self.request.user,
        )
        messages.success(self.request, "Movimiento de stock registrado.")
        return super().form_valid(form)


class ProductLookupView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("q", "").strip()
        products = Product.objects.filter(is_active=True)
        if query:
            products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))
        data = [
            {
                "id": product.id,
                "sku": product.sku,
                "name": product.name,
                "sale_price": str(product.sale_price),
                "category": product.category.name if product.category else "Sin categoria",
            }
            for product in products.select_related("category")[:20]
        ]
        return JsonResponse(data, safe=False)
