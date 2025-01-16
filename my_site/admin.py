from django.contrib import admin
from .models import User, Reservation
from django.utils.html import format_html

# Регистрируем модель User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'email', 'is_active', 'is_staff', 'is_registered', 'is_new')
    list_filter = ('is_registered', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'phone', 'email')

# Регистрируем модель Reservation
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'table_number', 'num_people', 'reservation_time', 'created_at')  # Параметры, которые видны в списке
    list_filter = ('reservation_time', 'table_number')  # Фильтры для упрощения поиска
    search_fields = ('user__username', 'table_number')  # Поиск по имени пользователя и номеру стола
    date_hierarchy = 'reservation_time'  # Иерархия по времени для удобства
    ordering = ('-created_at',)  # Сортировка по времени создания брони, от самых новых

    # class Media:
    #     css = {
    #         'all': ('admin/css/custom.css',)
    #     }
