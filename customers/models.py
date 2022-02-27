from django.db import models
from products.models import Product


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        db_table = 'customers'
        verbose_name = "Uttente"
        verbose_name_plural = "Uttenti"


class Cart(models.Model):
    custumer = models.OneToOneField(Customer, on_delete=models.CASCADE,
                                    related_name="cart")
    products = models.ManyToManyField(Product, related_name="carts")

    def __str__(self):
        return f"{self.product_id}"

    class Meta:
        db_table = 'carts'
        verbose_name = "Carrello"
        verbose_name_plural = "Carrelli"


