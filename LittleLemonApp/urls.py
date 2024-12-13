from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.MenuItemListView.as_view(), name='menu-items'),
]
