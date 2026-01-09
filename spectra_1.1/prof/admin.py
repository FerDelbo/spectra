from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserType, UserProfile

# Register your models here.
@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'funcoes')
    search_fields = ('nome',)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'

# Sobrescrever o UserAdmin para incluir o inline
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-registrar o UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
