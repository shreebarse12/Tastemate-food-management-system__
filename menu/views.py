# menu/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Dish
from .forms import DishForm
from .decorators import canteen_required  # or correct path
from django.views.decorators.http import require_POST


from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from orders.models import orders
from .forms import DishForm
from django.contrib.auth.decorators import login_required
from .decorators import canteen_required

@login_required
@canteen_required
def canteen_dashboard(request):
    # Which meal tab to show (defaults to breakfast)
    meal = request.GET.get('meal', 'breakfast')

    # Get the date to display. Defaults to today's date.
    date_str = request.GET.get('date')
    if date_str:
        try:
            served_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            served_date = timezone.localdate()
    else:
        served_date = timezone.localdate()

    # List dishes for the selected meal and date
    dishes = Dish.objects.filter(canteen=request.user, meal_type=meal, served_date=served_date).order_by('-created_at')

    # Handle the "Add Dish" form submission
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.canteen = request.user
            dish.save()
            messages.success(request, f"Dish '{dish.name}' added for {dish.served_date} ({dish.get_meal_type_display()}).")
            # Redirect to the same page to show the new dish
            return redirect(f"{reverse('canteen_dashboard')}?meal={meal}&date={served_date.isoformat()}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Pre-fill the form with the current date and meal type
        initial = {'served_date': served_date, 'meal_type': meal}
        form = DishForm(initial=initial)

    # Fetch only PENDING student orders for this canteen
    student_orders = orders.objects.filter(dish__canteen=request.user, status='pending').order_by('-ordered_at')

    # --- NEW LOGIC FOR "ALL MENUS" MODAL ---
    # Fetch all dishes for the logged-in canteen, ordered by date.
    all_dishes = Dish.objects.filter(canteen=request.user).order_by('-served_date', 'meal_type')
    
    # Group the dishes by their served date.
    all_menus_by_date = defaultdict(list)
    for dish in all_dishes:
        all_menus_by_date[dish.served_date].append(dish)
    # --- END OF NEW LOGIC ---

    context = {
        'dishes': dishes,
        'form': form,
        'meal': meal,
        'served_date': served_date,
        'student_orders': student_orders,
        # ADDED: Pass the date-grouped menus to the template for the modal
        'all_canteen_menus_by_date': dict(all_menus_by_date), 
    }
    return render(request, 'canteen_dashboard.html', context)


@login_required
@require_POST # Ensures this view only accepts POST requests
def update_order_status(request, order_id, status):
    """
    This view handles the canteen's action to accept or reject an order.
    """
    # Security check: Ensure the user is a canteen owner.
    if not request.user.is_canteen():
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')

    # Find the order, ensuring it belongs to a dish from THIS canteen.
    # This is a critical security fix.
    order = get_object_or_404(orders, id=order_id, dish__canteen=request.user)

    # Use lowercase for consistent checking.
    if status in ['accepted', 'rejected']:
        order.status = status
        order.save()
        messages.success(request, f"Order #{order.id} has been successfully {status}.")
    else:
        messages.error(request, "Invalid status update.")
    
    # Redirect back to the dashboard.
    return redirect('canteen_dashboard')






@login_required
@canteen_required
def edit_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk, canteen=request.user)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            messages.success(request, "Dish updated.")
            return redirect('dashboard')
    else:
        form = DishForm(instance=dish)
    return render(request, 'edit_dish.html', {'form': form, 'dish': dish})


@login_required
@canteen_required
def delete_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk, canteen=request.user)
    if request.method == 'POST':
        dish.delete()
        messages.success(request, "Dish deleted.")
        return redirect('dashboard')
    return render(request, 'menu/delete_dish_confirm.html', {'dish': dish})


# Student-facing: canteen's public menu (for students)
from django.shortcuts import render
from users.models import User

from math import radians, sin, cos, sqrt, atan2

# This is the Haversine formula to calculate distance between two lat/lon points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat / 2) * sin(dLat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) * sin(dLon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def public_menu(request):
    # Get the student's location from the URL query parameters
    student_lat = request.GET.get('lat')
    student_lon = request.GET.get('lon')

    # get all users who are canteens
    canteens = User.objects.filter(role=User.CANTEEN)
    
    canteen_menus = []
    for canteen in canteens:
        breakfast = Dish.objects.filter(canteen=canteen, meal_type="breakfast", available=True).order_by("-served_date")[:2]
        lunch = Dish.objects.filter(canteen=canteen, meal_type="lunch", available=True).order_by("-served_date")[:2]
        dinner = Dish.objects.filter(canteen=canteen, meal_type="dinner", available=True).order_by("-served_date")[:2]

        if breakfast.exists() or lunch.exists() or dinner.exists():
            # --- NEW: Calculate distance and attach it ---
            distance = None
            if student_lat and student_lon and canteen.latitude and canteen.longitude:
                try:
                    dist_km = haversine(
                        float(student_lat), float(student_lon),
                        canteen.latitude, canteen.longitude
                    )
                    distance = round(dist_km, 1) # Round to one decimal place
                except (ValueError, TypeError):
                    distance = None # Handle potential errors

            canteen_menus.append({
                "canteen": canteen,
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner,
                'distance': distance,  # Attach the calculated distance
            })

    # Optional: Sort the list of canteens by distance if available
    if student_lat and student_lon:
        canteen_menus.sort(key=lambda x: x['distance'] if x['distance'] is not None else float('inf'))

    return render(request, "canteen_public_menu.html", {"canteen_menus": canteen_menus})




from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from menu.models import Dish
from reviews.forms import ReviewForm
from reviews.models import Review

def canteen_detail(request, canteen_id):
    canteen = get_object_or_404(User, id=canteen_id, role=User.CANTEEN)

    breakfast = Dish.objects.filter(canteen=canteen, meal_type="breakfast", available=True).order_by("-served_date")
    lunch = Dish.objects.filter(canteen=canteen, meal_type="lunch", available=True).order_by("-served_date")
    dinner = Dish.objects.filter(canteen=canteen, meal_type="dinner", available=True).order_by("-served_date")

    # Handle Review form submission
    if request.method == "POST" and request.user.is_authenticated and request.user.is_student:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                student=request.user,
                canteen=canteen,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
            )
            return redirect('canteen_detail', canteen_id=canteen.id)
    else:
        form = ReviewForm()

    # Get all reviews for this canteen
    reviews = Review.objects.filter(canteen=canteen)

    context = {
        "canteen": canteen,
        "breakfast": breakfast,
        "lunch": lunch,
        "dinner": dinner,
        "reviews": reviews,
        "form": form,
    }
    return render(request, "canteen_detail.html", context)
