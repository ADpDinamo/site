from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from adpd.users.forms import UserChangeForm, UserCreationForm
from .models import UserRole

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("roles", "name", "mobile_number", "date_of_birth")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]

class UserRoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserRole, UserRoleAdmin)
