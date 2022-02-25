from django.db import models



class Product(models.Model):
    hash_summ = models.CharField(max_length=255, unique=True, default='')
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.01)
    availability = models.PositiveIntegerField(default=0)
    category = models.ForeignKey("Category",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="products")
    brand = models.ForeignKey("Brand", on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name = "Prodotto"
        verbose_name_plural = "Prodotti"


class Category(models.Model):
    cat_name = models.CharField(unique=True, db_index=True, max_length=40)
    
    def __str__(self):
        return self.cat_name
    class Meta:
        db_table = 'categories'
        verbose_name = "Categoria"
        verbose_name_plural = "Categorie"


class Brand(models.Model):
    model_name = models.CharField(unique=True, db_index=True, max_length=40)
    def __str__(self):
        return self.model_name
    class Meta:
        db_table = 'brands'
        verbose_name = "Marca"
        verbose_name_plural = "Marchi"


