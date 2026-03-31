from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'reference', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reference', 'order__id', 'order__user__email')
    readonly_fields = ('order', 'reference', 'amount', 'created_at')
    date_hierarchy = 'created_at'
