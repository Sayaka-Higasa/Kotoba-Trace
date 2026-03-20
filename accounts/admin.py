from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, PasswordReset

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "is_active", "is_staff", "created_at")
    fields = ("email", "name", "is_active", "is_staff", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

# パスワードリセットの履歴
@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ("user", "password_token", "is_used", "created_at")