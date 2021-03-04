# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import Session
from .models import Product
from .models import Category
from .models import Member


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']
    fieldsets = (
        (('User'), {'fields': ('username', 'email','is_staff', 'bio', 'timezone', 'startPage')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Session)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Member)