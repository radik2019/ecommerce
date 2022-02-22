from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.01)
    availability = models.PositiveIntegerField(default=0)


    class Meta:
        db_table = 'products'


