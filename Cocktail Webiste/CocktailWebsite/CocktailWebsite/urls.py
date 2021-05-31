from django.contrib import admin
from django.urls import path
from CocktailWebsite import views

urlpatterns = [
    path('', views.menu, name='menu'),

    path('login/', views.login, name='login'),
    path('verifyLogin/', views.verifylogin, name='verifylogin'),

    #path('profile/', views.profile, name='profile'),

    path('browse/', views.browse_cocktails, name='browse'),

    path('search/', views.search, name='search'),
    path('smembers/', views.smembers, name='smembers'),
    path('scocktails/', views.scocktails, name='scocktails'),

    path('admin/', admin.site.urls),

    path('searchcocktails/', views.searchcocktails, name='searchcocktails'),
    path('searchmembers/', views.searchmembers, name='searchmembers')

]