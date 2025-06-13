from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_account', 'get_service', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('charge__account__number', 'charge__account__user__username', 'charge__service__name')
    ordering = ('-date',)
    autocomplete_fields = ('charge',)

    def get_user(self, obj):
        return obj.charge.account.user
    get_user.short_description = 'Пользователь'
    get_user.admin_order_field = 'charge__account__user'

    def get_account(self, obj):
        return obj.charge.account
    get_account.short_description = 'Счёт'
    get_account.admin_order_field = 'charge__account'

    def get_service(self, obj):
        return obj.charge.service
    get_service.short_description = 'Услуга'
    get_service.admin_order_field = 'charge__service'
