from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from rest_framework_api_key.admin import APIKeyModelAdmin

from .models import QueUser, SocialLink, Education, UserAPIKeyModel, UserPhotos


class UserPhotosInline(admin.TabularInline):
    model = UserPhotos
    extra = 1


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
         {'fields': (
             'phone', 'smart_photos', 'birthday', 'city',
             'bio', 'gender', 'is_verified')}),
    )
    inlines = [UserPhotosInline]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('spotify', 'instagram')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('education',)


@admin.register(UserAPIKeyModel)
class UserAPIKeyBModelAdmin(APIKeyModelAdmin):
    pass
