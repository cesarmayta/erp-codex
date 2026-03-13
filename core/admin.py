from django.contrib import admin

from core.models import AuditLog, Branch, Warehouse, Sequence, BusinessSetting, Company

admin.site.register(Branch)
admin.site.register(Warehouse)
admin.site.register(Sequence)
admin.site.register(BusinessSetting)
admin.site.register(AuditLog)
admin.site.register(Company)
