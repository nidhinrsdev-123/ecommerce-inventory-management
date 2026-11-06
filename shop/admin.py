from django.contrib import admin
from .models import Product,Order,OrderItem
admin.site.register(Product)
class Items(admin.TabularInline):
 model=OrderItem; extra=0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
 list_display=("id","customer","status","total","created_at"); list_filter=("status","created_at"); inlines=[Items]
