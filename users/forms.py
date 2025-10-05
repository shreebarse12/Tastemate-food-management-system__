from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.STUDENT
        if commit:
            user.save()
        return user


class CanteenRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'canteen_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.CANTEEN
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

