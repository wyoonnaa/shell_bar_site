from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Phone', max_length=150)

    def clean_username(self):
        username_or_phone = self.cleaned_data['username']
        
        # Попробуем найти пользователя по имени
        user = User.objects.filter(username=username_or_phone).first()
        
        # Если не нашли, ищем по телефону
        if not user:
            user = User.objects.filter(phone=username_or_phone).first()
        
        if not user:
            raise forms.ValidationError("Пользователь с таким именем или номером телефона не найден.")
        
        return username_or_phone
