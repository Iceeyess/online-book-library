from django.contrib import admin
from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', )
    list_filter = ('id', 'username', 'email', )
    search_fields = ('first_name', 'last_name', 'email', 'username', 'id', )
