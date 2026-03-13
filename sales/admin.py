from django.contrib import admin

from sales.models import Customer, Sale, SaleLine, Payment

admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(SaleLine)
admin.site.register(Payment)
