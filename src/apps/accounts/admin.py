from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *



class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email",'phone','address','city')}),
        (_("confirms"), {"fields": ("email_confirmed","phone_confirmed","is_active")}),

        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )





class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user',)





admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Profile,ProfileAdmin)