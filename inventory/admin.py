from django.contrib import admin

from inventory.models import Category, Product, StockMovement, StockSnapshot

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(StockMovement)
admin.site.register(StockSnapshot)
