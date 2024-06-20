from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home'),
    path('login/',user_login, name='login'),
    path('register/',user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/',view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', update_cart_item, name='update_cart_item'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)