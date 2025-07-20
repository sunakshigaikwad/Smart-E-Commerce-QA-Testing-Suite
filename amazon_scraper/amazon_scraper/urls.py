from django.contrib import admin
from django.urls import path, include
from scraper import views
from django.shortcuts import render
from scraper.views import transaction_api



urlpatterns = [
     path('', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup_user, name='signup_user'),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    #path('', include('scraper.urls')),
    path('admin/', admin.site.urls),
    path('payment-success/', lambda request: render(request, 'payment_success.html'), name='payment_success'),
    path('payment/', views.payment, name='payment'),
    path('api/transactions/', transaction_api),


]
