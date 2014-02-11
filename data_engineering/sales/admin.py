from django.contrib import admin
from sales.models import (Merchant, Item, Billing, Sale)

admin.site.register(Merchant)
admin.site.register(Item)
admin.site.register(Billing)
admin.site.register(Sale)
