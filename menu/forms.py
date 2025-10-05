# menu/forms.py
from django import forms
from .models import Dish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'is_veg', 'available', 'meal_type', 'served_date', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dish name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_veg': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'served_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class PublicDishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'is_veg', 'meal_type', 'served_date', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dish name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_veg': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'served_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }