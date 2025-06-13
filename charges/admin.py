from django.contrib import admin
from .models import ServiceType, Charge
from payments.models import Payment

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ('amount', 'date')
    readonly_fields = ('amount', 'date')
    show_change_link = True

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_account', 'service', 'period', 'amount', 'status')
    list_filter = ('status', 'service', 'period')
    search_fields = ('account__number', 'account__user__username', 'service__name')
    ordering = ('-period', 'account')
    autocomplete_fields = ('account', 'service')
    inlines = [PaymentInline]

    def get_user(self, obj):
        return obj.account.user
    get_user.short_description = 'Пользователь'
    get_user.admin_order_field = 'account__user'

    def get_account(self, obj):
        return obj.account
    get_account.short_description = 'Счёт'
    get_account.admin_order_field = 'account'
