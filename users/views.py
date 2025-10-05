from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import  LoginForm
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.views import LoginView
from menu.views import public_menu, canteen_dashboard
from django.contrib.auth import logout
# Create your views here.
from .forms import StudentRegistrationForm, CanteenRegistrationForm

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')  # student dashboard/home
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register_student.html', {'form': form})


def register_canteen(request):
    if request.method == 'POST':
        form = CanteenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')  # canteen dashboard
    else:
        form = CanteenRegistrationForm()
    return render(request, 'registration/register_canteen.html', {'form': form})




def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == User.CANTEEN:
                login(request, user)
                return redirect('canteen_dashboard')
            elif user is not None and user.role == User.STUDENT:
                login(request, user)
                return redirect('public_menu')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})


def logout_view(request):
    """Custom logout for custom user model"""
    if request.user.is_authenticated:
        logout(request)  # clears the session
    return redirect('login_view')  # change 'login_view' to your login URL name

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def home(request):
    return render(request, 'home.html')

