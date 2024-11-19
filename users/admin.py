from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'name', 'is_staff', 'is_active',
                    'date_joined')  # Поля, которые будут отображаться в списке пользователей
    search_fields = ('email', 'username')  # Поля для поиска
    list_filter = ('is_staff', 'is_active')  # Фильтры для админки
    ordering = ('-date_joined',)  # Сортировка по дате регистрации (по убыванию)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    # Включаем возможность редактировать поля в админке
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal info', {
            'fields': ('name', 'avatar')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    # Редактируем только необходимые поля
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)