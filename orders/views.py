from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import orders
from menu.models import Dish

@login_required

def place_order(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        total_price = dish.price * quantity
        pickup_time = request.POST.get("pickup_time")  # pickup time from form
        if pickup_time:
            # Convert string to datetime object
            from datetime import datetime
            pickup_time = datetime.strptime(pickup_time, "%Y-%m-%dT%H:%M")
        
        orders.objects.create(
            student=request.user,
            dish=dish,
            quantity=quantity,
            total_price=total_price,
            pickup_time=pickup_time
        )
        return redirect("my_orders")

    return render(request, "place_order.html", {"dish": dish})

@login_required
def my_orders(request):
    order = orders.objects.filter(student=request.user).order_by("-ordered_at")
    return render(request, "my_orders.html", {"orders": order})

@login_required
def manage_orders(request):
    """For canteen users to accept/reject orders"""
    orders = orders.objects.filter(dish__canteen=request.user).order_by("-ordered_at")
    return render(request, "orders/manage_orders.html", {"orders": orders})


from django.contrib import messages

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(orders, id=order_id, student=request.user)
    
    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('my_orders')
    
    # Optional: If you want a confirmation page
    # return render(request, "orders/confirm_delete.html", {"order": order})
