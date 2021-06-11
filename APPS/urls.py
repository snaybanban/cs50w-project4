from django.conf.urls import url
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
	path('', views.index, name='index'),
	path('/visita', views.visita, name='visita'),
	path('/acerca', views.acerca, name='acerca'),
	path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('products/', views.products, name='products'),
	path('add_item', views.addItem_view, name='add_item'),
    path('remove_item/<int:cart_item_id>', views.removeItem_view, name='remove_item'),
    path('empty_cart', views.emptyCart_view, name='empty_cart'),
    path('cart', views.cart_view, name='cart'),
    path('order', views.order_view, name='order'),
    path('orders', views.orders_view, name='orders'),
    path('vieworders', views.viewOrders_view, name='vieworders'),
    path('markComplete/<int:order_item_id>', views.markComplete_view, name='markcomplete')
	
]