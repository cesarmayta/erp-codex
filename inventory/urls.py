from django.urls import path

from inventory.views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    ProductCreateView,
    ProductDeleteView,
    ProductListView,
    ProductUpdateView,
    StockMovementCreateView,
    StockMovementListView,
    StockSnapshotListView,
)

urlpatterns = [
    path("categorias/", CategoryListView.as_view(), name="category-list"),
    path("categorias/nuevo/", CategoryCreateView.as_view(), name="category-create"),
    path("categorias/<int:pk>/editar/", CategoryUpdateView.as_view(), name="category-update"),
    path("categorias/<int:pk>/eliminar/", CategoryDeleteView.as_view(), name="category-delete"),
    path("productos/", ProductListView.as_view(), name="product-list"),
    path("productos/nuevo/", ProductCreateView.as_view(), name="product-create"),
    path("productos/<int:pk>/editar/", ProductUpdateView.as_view(), name="product-update"),
    path("productos/<int:pk>/eliminar/", ProductDeleteView.as_view(), name="product-delete"),
    path("stock/", StockSnapshotListView.as_view(), name="stock-list"),
    path("movimientos/", StockMovementListView.as_view(), name="stock-movement-list"),
    path("movimientos/nuevo/", StockMovementCreateView.as_view(), name="stock-movement-create"),
]
