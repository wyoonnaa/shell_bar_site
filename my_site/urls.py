from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.index, name='index'),  # главная страница
    path('about/', views.about, name='about'),  # страница "О нас"
    path('contacts/', views.contacts, name='contacts'),  # страница "Контакты"
    path('registration/', views.registration, name='registration'), # страница регистрации
    path('alco/', views.alco, name='alco'),  # страница "Бар"
    path('coct/', views.coct, name='coct'),  # страница "Коктейли"
    path('food/', views.food, name='food'),  # страница "Еда"
    path('guest_dashboard/<int:user_id>/', views.guest_dashboard, name='guest_dashboard'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    
]




if settings.DEBUG:  # Только для разработки
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
