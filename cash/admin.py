from django.contrib import admin

from cash.models import CashEntry, CashRegister, CashSession

admin.site.register(CashRegister)
admin.site.register(CashSession)
admin.site.register(CashEntry)
