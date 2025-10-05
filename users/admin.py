
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = User

#     list_display = ('username', 'email', 'role', 'is_staff')
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('role', 'phone', 'address', 'canteen_name')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('role', 'phone', 'address', 'canteen_name')}),
#     )

admin.site.register(User)
