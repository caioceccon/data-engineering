from django.contrib import admin
from sales.models import (Merchant, Item, Billing, Sale)


class BillingAdmin(admin.ModelAdmin):
    list_display = ('txtBillingFile', 'calculate_gross_revenue')


admin.site.register(Merchant)
admin.site.register(Item)
admin.site.register(Billing, BillingAdmin)
admin.site.register(Sale)
