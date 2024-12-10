from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
import datetime
from django.utils import timezone


class Product(models.Model):
    publication_date = models.DateTimeField("Date of publication")
    product_text = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    image = models.ImageField(null=True, blank=True, upload_to='products/')

    def __str__(self):
        return self.product_text

    @admin.display(
        boolean=True,
        ordering="publication_date",
        description="Was it published recently?",
    )
    def published_recently(self): # not necessary?
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publication_date <= now


class Position(models.Model):
    description = models.CharField(max_length = 300, blank = False)
    name = models.CharField(max_length = 300, blank = False)

    def __str__(self):
        return str(self.name)


class Person(models.Model):
    surname = models.CharField(max_length = 100, blank = False)
    name = models.CharField(max_length = 100, blank = False)

    class Sex(models.IntegerChoices):
        Female = 0
        Male = 1

    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    sex = models.IntegerField(choices=Sex.choices, default=1)
    date_added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @admin.display
    def position_id(self):
        return (str(self.position.name) + str(self.position.id))

    class Meta:
        ordering = ["surname"]
        permissions = [
            ("can_view_other_persons", "Can view other persons"),  # Custom permission
        ]
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return str(self.name + " " + self.surname)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_text} x {self.quantity}"


