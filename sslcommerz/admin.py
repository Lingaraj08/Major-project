from django.contrib import admin
from .models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'patient', 'payment_type', 'status', 'currency_amount', 'transaction_date')
    list_filter = ('payment_type', 'status', 'transaction_date')
    search_fields = ('invoice_number', 'transaction_id', 'email', 'patient__name')
    readonly_fields = ('payment_id', 'transaction_id', 'val_transaction_id')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'invoice_number', 'payment_type', 'status')
        }),
        ('Customer Details', {
            'fields': ('patient', 'name', 'email', 'phone', 'address', 'city', 'country')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'val_transaction_id', 'currency_amount', 'currency', 'transaction_date')
        }),
        ('Service Details', {
            'fields': ('appointment', 'order', 'test_order', 'prescription', 'consulation_fee', 'report_fee')
        }),
        ('Payment Method Details', {
            'fields': ('card_type', 'card_no', 'card_issuer', 'card_brand', 'bank_transaction_id')
        }),
    )
