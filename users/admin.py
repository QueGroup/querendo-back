from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from image_uploader_widget.admin import ImageUploaderInline

from users.models import (
    profiles,
    filters,
    photos
)
from users.models.users import User


class ProfileAdminInline(admin.StackedInline):
    model = profiles.Profile
    fields = (
        'gender',
        'age',
        'country',
        'city',
        'latitude',
        'longitude',
        'date_of_birth',
        'occupation',
        'ideal_match',
        'interests'
    )


class FilterAdminInline(admin.StackedInline):
    model = filters.Filters
    fields = (
        'radius',
        'gender',
        'min_age',
        'max_age',
    )


class PhotoInline(ImageUploaderInline):
    model = photos.UserPhotos


@admin.register(photos.UserPhotos)
class UserPhotosAdmin(admin.ModelAdmin):
    pass


@admin.register(profiles.Interest)
class UserInterestAdmin(admin.ModelAdmin):
    model = profiles.Interest
    list_display = ('id', 'name',)


@admin.register(photos.BrandBook)
class BrandBookAdmin(admin.ModelAdmin):
    model = photos.BrandBook
    list_display = ('id', 'name_of_page', 'photo',)


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'telegram_id')}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'full_name', 'email', 'phone_number',)

    list_display_links = ('id', 'full_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)

    inlines = (ProfileAdminInline, PhotoInline, FilterAdminInline)
