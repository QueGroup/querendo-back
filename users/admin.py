from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from image_uploader_widget.admin import ImageUploaderInline

from users.models import filters, interests, photos
from users.models.users import User


# fields = (
#         'gender',
#         'age',
#         'country',
#         'city',
#         'latitude',
#         'longitude',
#         'date_of_birth',
#         'occupation',
#         'ideal_match',
#         'interests'
#     )

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


@admin.register(interests.Interest)
class UserInterestAdmin(admin.ModelAdmin):
    model = interests.Interest
    list_display = ('id', 'name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('phone_number', 'username', 'telegram_id')}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Important dates'), {'fields': ('created_at', 'updated_at',)}),
    )
    list_display = ('id', 'username', 'phone_number',)
    list_display_links = ('id', 'username',)
    search_fields = ('first_name', 'last_name', 'id', 'phone_number',)
    ordering = ('-id',)

    inlines = (PhotoInline, FilterAdminInline)
