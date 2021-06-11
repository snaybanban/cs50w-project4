import re
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
#from .forms import UserRegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def visita(request):
    return render(request, 'indexx.html')

def acerca(request):
    return render(request, 'acerca.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form =  CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'se ha creado la cuenta de' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'RegistrarUser.html', context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = authenticate(request, username = username, password = password)

        if users is not None:
            login(request, users)
            return redirect('index')
        else:
            messages.info(request, 'contrasena incorrecta')

    context = {}
    return render(request, 'login.html', context)

def logoutpage(request):
    logout(request)
    return redirect("index")

def products(request):
    if request.user.is_authenticated:
        context = {
        'item_cats': Item_Category.objects.all(),
        'items': Item.objects.all(),
        'toppings': Topping.objects.all()
    }
        return render(request, 'productos.html', context)
    else:
        return redirect('login')

def addItem_view(request):
    
    if request.method == 'POST':
        try:
            item_id = request.POST['item-id']
        except:
            item_id = None
        try:
            max_topping = request.POST['max-topping']
        except:
            max_topping = None
        try:
            size = request.POST['size-select']
        except:
            size = None
        
        toppings = []
        if max_topping:
            for i in max_topping:
                try:
                    top = request.POST[f'select-{i}']
                    toppings.append(Topping.objects.get(pk=top))
                except:
                    pass

        item = Item.objects.get(pk=item_id)
        if size == 'S':
            price = item.price_small
        elif size == 'L':
            price = item.price_large
            
        print(request.user)
        cart = Cart.objects.get(user=request.user)
        cart_item = Cart_Item(cart=cart, item_detail=item, size=size, price=price)
        cart_item.save()
        if len(toppings) > 0:
            for topping in toppings:
                cart_item.topping.add(topping)
            cart_item.save()
        cart.total += cart_item.price
        cart.save()
    messages.success(request, 'Orden registrada')
    return HttpResponseRedirect(reverse('products'))

def removeItem_view(request, cart_item_id):
    cart_item = Cart_Item.objects.get(pk=cart_item_id)
    cart = Cart.objects.get(user=request.user)
    cart.total -= cart_item.price
    cart_item.delete()
    cart.save()
    messages.success(request, messages.INFO, f'Item {cart_item.item_detail} removido!')
    return HttpResponseRedirect(reverse('cart'))

def emptyCart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart.total = 0
    cart.save()
    cart_items = Cart_Item.objects.filter(cart=cart)
    if cart_items:
        for cart_item in cart_items:
            cart_item.delete()
    messages.success(request, 'Limpió su carrito')
    return HttpResponseRedirect(reverse('cart'))

def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = Cart_Item.objects.filter(cart=cart)
    if not cart_items:
        return render(request, 'cart.html', {'empty': True})
    return render(request, 'cart.html', {'empty': False, 'cart_items': cart_items, 'cart':cart})

def order_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items =  Cart_Item.objects.filter(cart=cart)

    #create a new empty order
    order = Order(user=request.user, total=cart.total)
    order.save()

    for cart_item in cart_items:
        order_item = Order_Item(order=order, item_detail=cart_item.item_detail, size=cart_item.size, price=cart_item.price)
        order_item.save()
        order_item.topping.set(cart_item.topping.all())
        order_item.save()
    messages.success(request, 'colocado con éxito')
    emptyCart_view(request)
    return HttpResponseRedirect(reverse('products'))

def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    if not orders:
        return render(request, 'orders.html', {'empty': True})
    dic = dict()
    for order in orders:
        order_items = Order_Item.objects.filter(order=order)
        dic.update({order: order_items})

    return render(request, 'orders.html', {'empty': False, 'dic': dic})

def viewOrders_view(request):
    if request.method == 'POST':
        pass
    else:
        if request.user.is_staff:
            orders = Order.objects.exclude(status='Completed')
            if not orders:
                return render(request, 'vieworders.html', {'empty': True})
            dic = dict()
            for order in orders:
                order_items = Order_Item.objects.filter(order=order)
                dic.update({order: order_items})

            return render(request, 'vieworders.html', {'empty': False, 'dic': dic})

def markComplete_view(request, order_item_id):
    order = Order.objects.get(pk=order_item_id)
    order.status = 'Completed'
    order.save()
    messages.add_message(request, messages.SUCCESS, f'Marked Order #{order.pk} as completed')
    return HttpResponseRedirect(reverse('vieworders'))



