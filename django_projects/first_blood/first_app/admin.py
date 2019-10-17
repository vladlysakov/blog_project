from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User_Profile
from .forms import UserForm

class UsersAdmin(UserAdmin):
    add_form = UserForm
    list_display = ('username', 'email', 'last_login')
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Dates', {'fields': ('last_login', 'date_joined', 'logout_time', 'session_time', 'time_last_logout')}),
        )


admin.site.register(User_Profile, UsersAdmin)

