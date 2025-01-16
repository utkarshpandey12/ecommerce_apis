from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name

    def deduct_product_stock(self, quantity: int):
        self.stock -= quantity
        self.save()


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
    )
    products = models.JSONField()
    total_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
