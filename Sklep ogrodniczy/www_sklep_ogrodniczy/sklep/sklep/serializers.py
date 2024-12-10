from rest_framework import serializers
from .models import Person, Position, Product, Cart, CartItem
from datetime import datetime
from django.contrib.auth.models import User


class UserRegistrationModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs): # password at least 6 chars long
        if 'password' in attrs and len(attrs['password']) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data): # option to change email / password in the future
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class PositionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["id", "name", "description"]

    def validate(self, attrs): # name and description must not be empty!
        if 'name' in attrs and len(attrs['name'].strip()) == 0:
            raise serializers.ValidationError("Position name cannot be empty.")
        if 'description' in attrs and len(attrs['description'].strip()) == 0:
            raise serializers.ValidationError("Position description cannot be empty.")
        return attrs

    def create(self, validated_data):
        return Position.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ProductModelSerializer(serializers.Serializer):
    product_text = serializers.CharField(max_length=400)
    publication_date = serializers.DateTimeField("Date of publication")
    price = serializers.DecimalField(max_digits=30, decimal_places=2)

    class Meta:
        model = Product
        fields = ['id', 'publication_date', 'product_text', 'price', 'image']

    def validate_product_text(self, value): # product text at least 3 chars long
        if len(value) < 3:
            raise serializers.ValidationError("Product text must be at least 3 characters long.")
        return value

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.product_text = validated_data.get('product_text', instance.product_text)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class PersonModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    position = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Person
        fields = ["id", "name", "surname", "sex", "position", "date_added", "owner"]

    def validate_name(self, value): # only letters
        if not value.isalpha():
            raise serializers.ValidationError("Only letters allowed in name.")
        return value

    def validate_surname(self, value): # only letters
        if not value.isalpha():
            raise serializers.ValidationError("Only letters allowed in surname.")
        return value

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.sex = validated_data.get("sex", instance.sex)
        instance.position = validated_data.get("position", instance.position)
        instance.owner = validated_data.get("owner", instance.owner)
        instance.save()
        return instance


class CartItemModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'cart']

    def validate(self, attrs): # at least one item
        if 'quantity' in attrs and attrs['quantity'] < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return attrs

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.cart = validated_data.get('cart', instance.cart)
        instance.save()
        return instance


class CartModelSerializer(serializers.ModelSerializer):
    items = CartItemModelSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
