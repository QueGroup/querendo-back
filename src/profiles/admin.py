from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import UserQue
from .models import Interests
from .models import City
from .models import Gender
from .models import UserAssumption



class UserQueAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Info'), {'fields': ('phone', 'avatar', 'gender', 'favorite_categories')}),
    )


admin.site.register(UserQue, UserQueAdmin)
admin.site.register(Interests)
admin.site.register(City)
admin.site.register(Gender)
admin.site.register(UserAssumption)
