from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import QueUser, SocialLink, Profile


@admin.register(QueUser)
class QueUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'first_name', 'is_staff', 'get_image')
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

    @staticmethod
    def get_image(obj):
        return mark_safe('<img src={img} width="50" height="60"'.format(img=obj.avatar.url))


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "spotify", "instagram")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "bio",
        "smart_photos",
        "relation_goals",
        "zodiac_sign",
        "education",
        "personality_type",
        "city",
        "company",
    )
