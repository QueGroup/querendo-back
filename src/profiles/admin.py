from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import QueUser, SocialLink, Gender, Education, InterestedInGender, UserPhoto


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
             'phone', 'gender_id', 'education_id', "interests_in_gender_id", "smart_photos", "birthday", "city",
             "bio")}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("user_account_id", "spotify", "instagram")


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(InterestedInGender)
class InterestedInGenderAdmin(admin.ModelAdmin):
    list_display = ('gender_id',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin):
    list_display = ('user_account_id', 'photo',)
