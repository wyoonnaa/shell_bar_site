from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError



class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_registered = models.BooleanField(default=False)

    def is_new(self):
        return self.date_joined >= now() - timedelta(days=1)

    is_new.boolean = True 
    is_new.short_description = "Новый пользователь"


class Reservation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="User"
    )
    table_number = models.PositiveIntegerField(verbose_name="Table number")
    num_people = models.PositiveIntegerField(verbose_name="Number of people")
    reservation_time = models.DateTimeField(verbose_name="Reservation time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ["-created_at"]
        unique_together = ('table_number', 'reservation_time')

    def clean(self):
        if self.reservation_time < now():
            raise ValidationError("Нельзя бронировать в прошлом времени.")
        if not (1 <= self.num_people <= 20):
            raise ValidationError("Количество человек должно быть от 1 до 20.")

    def __str__(self):
        return f"Reservation by {self.user.username} for table {self.table_number} at {self.reservation_time}"