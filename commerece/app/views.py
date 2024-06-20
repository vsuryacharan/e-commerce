from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart,created= Cart.objects.get_or_create(user=request.user)
    cart_item,created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # Only increment the quantity if the cart_item already existed
        cart_item.quantity += 1
    
    cart_item.save()
    return redirect('home')

@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()  # Delete item if quantity is set to 0 or less
            except ValueError:
                pass  # Handle the case where quantity is not an integer
    
    return redirect('view_cart')