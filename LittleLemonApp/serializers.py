from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem, CartItem, Order

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), source='menu_item', write_only=True)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    item_ids = serializers.PrimaryKeyRelatedField(queryset=CartItem.objects.all(), source='items', many=True, write_only=True)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Order
        fields = '__all__'

    def validate_item_ids(self, value):
        for item_id in value:
            if not CartItem.objects.filter(id=item_id.id).exists():
                raise serializers.ValidationError(f"Invalid pk \"{item_id.id}\" - object does not exist.")
        return value

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order.items.set(items)
        return order