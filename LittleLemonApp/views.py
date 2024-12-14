from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem
from django.http import HttpResponseRedirect
from rest_framework import generics, status, mixins
from rest_framework.pagination import PageNumberPagination
from .serializers import MenuItemSerializer
from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions, filters
from .models import MenuItem, CartItem, Order
from .serializers import MenuItemSerializer, UserSerializer, CartItemSerializer, OrderSerializer
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from django.contrib.auth import logout
from django.shortcuts import redirect

def home(request):
    return render(request, 'home.html')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'menu-items': {
            'list': reverse('menuitem-list', request=request, format=format),
            'detail': reverse('menuitem-detail', args=[1], request=request, format=format) + '{id}/'
        },
        'users': {
            'list': reverse('user-list', request=request, format=format),
            'detail': reverse('user-detail', args=[1], request=request, format=format) + '{id}/'
        },
        'cart-items': {
            'list': reverse('cartitem-list', request=request, format=format),
            'detail': reverse('cartitem-detail', args=[1], request=request, format=format) + '{id}/'
        },
        'orders': {
            'list': reverse('order-list', request=request, format=format),
            'detail': reverse('order-detail', args=[1], request=request, format=format) + '{id}/'
        },
    })

class MenuItemPagination(PageNumberPagination):
    page_size = 5

class MenuItemViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['price', 'name']
    filterset_fields = ['available', 'category']
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']
    filterset_fields = ['is_active', 'is_staff']
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['menu_item__name', 'user__username']
    ordering_fields = ['quantity', 'menu_item__name']
    filterset_fields = ['user', 'menu_item']
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__username', 'status']
    ordering_fields = ['status', 'created_at']
    filterset_fields = ['status', 'user']
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]

def admin_logout(request):
    logout(request)
    return redirect('/admin/')

def api_logout(request):
    logout(request)
    return redirect('/api/')
