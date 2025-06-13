from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User
from accounts.models import Account


class AccountInline(admin.TabularInline):
    model = Account
    extra = 0
    fields = ('number', 'address', 'is_active')
    readonly_fields = ('number',)
    show_change_link = True

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('full_name', 'address', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'address', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'full_name', 'email', 'address', 'is_staff', 'is_active')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('username',)

    inlines = [AccountInline]
