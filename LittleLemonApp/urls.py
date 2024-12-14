from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menu-items', views.MenuItemViewSet, basename='menuitem')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('cart-items/', views.CartItemListView.as_view(), name='cartitem-list'),
    path('cart-items/<int:pk>/', views.CartItemDetailView.as_view(), name='cartitem-detail'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('groups/<str:group_name>/users', views.add_user_to_group, name='add-user-to-group'),
    path('groups/<str:group_name>/users', views.list_group_users, name='list-group-users'),
]
