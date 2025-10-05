# loginss/decorators.py
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

def canteen_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # or your login url
        if getattr(request.user, 'role', None) in ('CANTEEN', 'canteen', 'Canteen'):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Only canteen accounts can access that page.")
        return redirect('home')  # fallback for students
    return _wrapped

