from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import QueUser, SocialLink


@admin.register(QueUser)
class QueUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'first_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Info'),
         {'fields': ('phone', 'gender', 'educational_experience', 'show_me', 'interests', 'avatar', 'birthday')}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "spotify", "instagram")
