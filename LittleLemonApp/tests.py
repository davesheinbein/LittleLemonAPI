from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import MenuItem, CartItem, Order

class MenuItemModelTest(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Test Item",
            description="Test Description",
            price=10.00
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, "Test Item")
        self.assertEqual(self.menu_item.description, "Test Description")
        self.assertEqual(self.menu_item.price, 10.00)

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.menu_item = MenuItem.objects.create(name="Test Item", description="Test Description", price=10.00)
        self.cart_item = CartItem.objects.create(user=self.user, menu_item=self.menu_item, quantity=2)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.user.username, "testuser")
        self.assertEqual(self.cart_item.menu_item.name, "Test Item")
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.get_total_price(), 20.00)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.menu_item = MenuItem.objects.create(name="Test Item", description="Test Description", price=10.00)
        self.cart_item = CartItem.objects.create(user=self.user, menu_item=self.menu_item, quantity=2)
        self.order = Order.objects.create(user=self.user, status="Pending")
        self.order.items.add(self.cart_item)

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.status, "Pending")
        self.assertEqual(self.order.get_total_order_price(), 20.00)

class MenuItemListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu_item = MenuItem.objects.create(
            name="Test Item",
            description="Test Description",
            price=9.99
        )

    def test_get_menu_items(self):
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.menu_item.name)

    def test_create_menu_item(self):
        data = {"name": "New Item", "description": "New Description", "price": 5.99}
        response = self.client.post(reverse('menu-items'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)
        self.assertEqual(MenuItem.objects.get(id=2).name, "New Item")

class CartItemListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.menu_item1 = MenuItem.objects.create(name="Item 1", description="Description 1", price=1.99)
        self.menu_item2 = MenuItem.objects.create(name="Item 2", description="Description 2", price=2.99)

    def test_bulk_create_cart_items(self):
        data = [
            {"menu_item_id": self.menu_item1.id, "quantity": 2, "user": "user1"},
            {"menu_item_id": self.menu_item2.id, "quantity": 1, "user": "user2"}
        ]
        response = self.client.post(reverse('cart-items'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)
        self.assertEqual(CartItem.objects.get(id=1).user.username, "user1")
        self.assertEqual(CartItem.objects.get(id=2).user.username, "user2")

class UserListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_bulk_create_users(self):
        data = [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"},
            {"username": "user3", "email": "user3@example.com"},
            {"username": "user4", "email": "user4@example.com"},
            {"username": "user5", "email": "user5@example.com"}
        ]
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(User.objects.get(username="user1").email, "user1@example.com")
        self.assertEqual(User.objects.get(username="user2").email, "user2@example.com")
        self.assertEqual(User.objects.get(username="user3").email, "user3@example.com")
        self.assertEqual(User.objects.get(username="user4").email, "user4@example.com")
        self.assertEqual(User.objects.get(username="user5").email, "user5@example.com")

class OrderListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")
        self.user4 = User.objects.create(username="user4")
        self.user5 = User.objects.create(username="user5")
        self.menu_item1 = MenuItem.objects.create(name="Item 1", description="Description 1", price=1.99)
        self.menu_item2 = MenuItem.objects.create(name="Item 2", description="Description 2", price=2.99)
        self.menu_item3 = MenuItem.objects.create(name="Item 3", description="Description 3", price=3.99)
        self.menu_item4 = MenuItem.objects.create(name="Item 4", description="Description 4", price=4.99)
        self.menu_item5 = MenuItem.objects.create(name="Item 5", description="Description 5", price=5.99)
        self.menu_item6 = MenuItem.objects.create(name="Item 6", description="Description 6", price=6.99)
        self.menu_item7 = MenuItem.objects.create(name="Item 7", description="Description 7", price=7.99)
        self.menu_item8 = MenuItem.objects.create(name="Item 8", description="Description 8", price=8.99)
        self.menu_item9 = MenuItem.objects.create(name="Item 9", description="Description 9", price=9.99)
        self.menu_item10 = MenuItem.objects.create(name="Item 10", description="Description 10", price=10.99)
        self.cart_item1 = CartItem.objects.create(user=self.user1, menu_item=self.menu_item1, quantity=2)
        self.cart_item2 = CartItem.objects.create(user=self.user2, menu_item=self.menu_item2, quantity=1)
        self.cart_item3 = CartItem.objects.create(user=self.user3, menu_item=self.menu_item3, quantity=3)
        self.cart_item4 = CartItem.objects.create(user=self.user4, menu_item=self.menu_item4, quantity=1)
        self.cart_item5 = CartItem.objects.create(user=self.user5, menu_item=self.menu_item5, quantity=2)
        self.cart_item6 = CartItem.objects.create(user=self.user1, menu_item=self.menu_item6, quantity=1)
        self.cart_item7 = CartItem.objects.create(user=self.user2, menu_item=self.menu_item7, quantity=1)
        self.cart_item8 = CartItem.objects.create(user=self.user3, menu_item=self.menu_item8, quantity=1)
        self.cart_item9 = CartItem.objects.create(user=self.user4, menu_item=self.menu_item9, quantity=1)
        self.cart_item10 = CartItem.objects.create(user=self.user5, menu_item=self.menu_item10, quantity=1)

    def test_bulk_create_orders(self):
        data = [
            {"item_ids": [self.cart_item1.id, self.cart_item2.id], "status": "pending", "user": "user1"},
            {"item_ids": [self.cart_item3.id, self.cart_item4.id], "status": "shipped", "user": "user2"},
            {"item_ids": [self.cart_item5.id, self.cart_item6.id], "status": "delivered", "user": "user3"},
            {"item_ids": [self.cart_item7.id, self.cart_item8.id], "status": "pending", "user": "user4"},
            {"item_ids": [self.cart_item9.id, self.cart_item10.id], "status": "canceled", "user": "user5"}
        ]
        response = self.client.post(reverse('orders'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 5)
        self.assertEqual(Order.objects.get(id=1).user.username, "user1")
        self.assertEqual(Order.objects.get(id=2).user.username, "user2")
        self.assertEqual(Order.objects.get(id=3).user.username, "user3")
        self.assertEqual(Order.objects.get(id=4).user.username, "user4")
        self.assertEqual(Order.objects.get(id=5).user.username, "user5")
