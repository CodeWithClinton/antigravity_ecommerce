from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False # Protect historic items natively

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('user__email', 'user__username', 'id')
    readonly_fields = ('user', 'total_amount', 'created_at')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at' # Streamlines timeframe drill-downs
    list_editable = ('status', 'payment_status')
