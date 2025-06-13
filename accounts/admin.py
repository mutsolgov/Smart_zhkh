from django.contrib import admin
from .models import Account
from charges.models import Charge

class ChargeInline(admin.TabularInline):
    model = Charge
    extra = 0
    fields = ('service', 'period', 'amount', 'status')
    readonly_fields = ('service', 'period', 'amount', 'status')
    show_change_link = True
    autocomplete_fields = ('service',)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'owner_full_name', 'address', 'area', 'residents_count', 'managing_company', 'is_active')
    list_filter = ('is_active', 'managing_company')
    search_fields = ('number', 'owner_full_name', 'address', 'user__username')
    ordering = ('user', 'number')
    autocomplete_fields = ('user',)
    inlines = [ChargeInline]
