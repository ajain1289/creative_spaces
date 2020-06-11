from django.contrib import admin
from backend_app.models import UserRole, RoleDetails, Categories, ProductDetails, TemporaryCart, Sales, InvoiceTable

admin.site.register(UserRole)
admin.site.register(RoleDetails)
admin.site.register(Categories)
admin.site.register(ProductDetails)
admin.site.register(TemporaryCart)
admin.site.register(Sales)
admin.site.register(InvoiceTable)
