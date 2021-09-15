"""django_wishlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = "wish_app"

urlpatterns = [
    path('', views.root),
    path('main', views.main, name='main'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('wish_items/create', views.create, name='create'),
    path('create_item', views.create_item, name='create_item'),
    path('wish_items/<item_id>', views.wish_items, name='wish_items'),
    path('erase_wish/<item_id>', views.erase_wish, name='erase_wish'),
    path('assign/<item_id>', views.assign, name='assign'),
    path('remove_wish/<item_id>', views.remove_wish, name='remove_wish'),
]


