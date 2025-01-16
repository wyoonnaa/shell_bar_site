from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now, localtime
from datetime import datetime
from .models import User, Reservation
from django.http import HttpResponseForbidden
from django.utils.timezone import make_aware, is_naive
from django.db.models import Count
from datetime import timedelta


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        phone = request.POST.get('phone').strip()

        if username == 'Admin' and phone == '+1234':
            return redirect('/admin/')

        user = User.objects.filter(username=username).first()
        if user:
            messages.info(request, 'Пользователь уже существует, перенаправляем в кабинет.')
            return redirect('guest_dashboard', user_id=user.id)
        
        try:
            new_user = User.objects.create(username=username, phone=phone, is_registered=True)
            messages.success(request, 'Пользователь успешно создан!')
            return redirect('guest_dashboard', user_id=new_user.id)
        except IntegrityError:
            messages.error(request, 'Ошибка: пользователь с таким именем уже существует.')
            return redirect('registration')

    return render(request, 'my_site/registration.html')



def guest_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    reservations = user.reservations.all()

    if request.method == 'POST':
        try:
            # Получаем данные из формы
            table_number = int(request.POST.get('table_number'))
            num_people = int(request.POST.get('num_people'))
            reservation_time_str = request.POST.get('reservation_time')

            # Парсим строку времени из формы
            reservation_time = datetime.strptime(reservation_time_str, '%Y-%m-%dT%H:%M')

            # Приводим reservation_time к offset-aware, если оно offset-naive
            if is_naive(reservation_time):
                reservation_time = make_aware(reservation_time)

            # Сравнение с текущим временем (уже offset-aware)
            if reservation_time < now():
                messages.error(request, "Нельзя выбрать дату и время в прошлом.")
                return redirect('guest_dashboard', user_id=user_id)

            # Проверяем, занято ли время
            if Reservation.objects.filter(table_number=table_number, reservation_time=reservation_time).exists():
                messages.error(request, "Этот стол уже забронирован на выбранное время.")
                return redirect('guest_dashboard', user_id=user_id)

            # Ограничение: не более двух столов на день
            reservations_for_day = user.reservations.filter(
                reservation_time__date=reservation_time.date()
            ).count()

            if reservations_for_day >= 2:
                messages.error(request, "Вы не можете забронировать более двух столов в один день.")
                return redirect('guest_dashboard', user_id=user_id)

            # Ограничение на минимальный интервал 3 часа между бронированиями
            for reservation in reservations:
                time_diff = abs(reservation_time - reservation.reservation_time)
                if time_diff < timedelta(hours=3):
                    messages.error(request, "Между вашими бронями должно быть не менее трех часов.")
                    return redirect('guest_dashboard', user_id=user_id)

            # Создаем новую бронь
            Reservation.objects.create(
                user=user,
                table_number=table_number,
                num_people=num_people,
                reservation_time=reservation_time
            )
            messages.success(request, "Стол успешно забронирован!")
        except ValueError as e:
            messages.error(request, f"Ошибка формата даты и времени: {str(e)}")
        except Exception as e:
            messages.error(request, f"Произошла ошибка: {str(e)}")
        return redirect('guest_dashboard', user_id=user_id)

    return render(request, 'my_site/guest_dashboard.html', {
        'user': user,
        'reservations': reservations,
        'current_time': localtime(now()).strftime('%Y-%m-%dT%H:%M')  # Формат для datetime-local
    })

# def guest_dashboard(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     reservations = user.reservations.all()

#     if request.method == 'POST':
#         try:
#             # Получаем данные из формы
#             table_number = int(request.POST.get('table_number'))
#             num_people = int(request.POST.get('num_people'))
#             reservation_time_str = request.POST.get('reservation_time')

#             # Парсим строку времени из формы
#             reservation_time = datetime.strptime(reservation_time_str, '%Y-%m-%dT%H:%M')

#             # Приводим reservation_time к offset-aware, если оно offset-naive
#             if is_naive(reservation_time):
#                 reservation_time = make_aware(reservation_time)

#             # Сравнение с текущим временем (уже offset-aware)
#             if reservation_time < now():
#                 messages.error(request, "Нельзя выбрать дату и время в прошлом.")
#                 return redirect('guest_dashboard', user_id=user_id)

#             # Проверяем, занято ли время
#             if Reservation.objects.filter(table_number=table_number, reservation_time=reservation_time).exists():
#                 messages.error(request, "Этот стол уже забронирован на выбранное время.")
#                 return redirect('guest_dashboard', user_id=user_id)

#             # Создаем новую бронь
#             Reservation.objects.create(
#                 user=user,
#                 table_number=table_number,
#                 num_people=num_people,
#                 reservation_time=reservation_time
#             )
#             messages.success(request, "Стол успешно забронирован!")
#         except ValueError as e:
#             messages.error(request, f"Ошибка формата даты и времени: {str(e)}")
#         except Exception as e:
#             messages.error(request, f"Произошла ошибка: {str(e)}")
#         return redirect('guest_dashboard', user_id=user_id)

#     return render(request, 'my_site/guest_dashboard.html', {
#         'user': user,
#         'reservations': reservations,
#         'current_time': localtime(now()).strftime('%Y-%m-%dT%H:%M')  # Формат для datetime-local
#     })

@login_required
def cancel_reservation(request, reservation_id):
    # Находим конкретную бронь по ID
    reservation = get_object_or_404(Reservation, id=reservation_id)
    # Удаляем только эту бронь
    reservation.delete()
    # Отправляем сообщение об успешном удалении
    messages.success(request, 'Бронь успешно удалена!')

    # Перенаправляем на гостевую панель пользователя
    return redirect('guest_dashboard', user_id=reservation.user.id)

def index(request):
    return render(request, 'my_site/index.html')

def about(request):
    return render(request, 'my_site/about.html')

def contacts(request):
    return render(request, 'my_site/contacts.html')


def alco(request):
    return render(request, 'my_site/alco.html')

def coct(request):
    return render(request, 'my_site/coct.html')

def food(request):
    return render(request, 'my_site/food.html')

