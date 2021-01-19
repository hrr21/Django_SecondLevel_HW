from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="имя продукта", max_length=256)
    image = models.ImageField(upload_to='products_images', blank=True)
    description = models.TextField(verbose_name="описание продукта",blank=True)
    short_description = models.CharField(verbose_name="краткое описание продукта",max_length=64, blank=True)
    price = models.DecimalField(verbose_name="цена продукта", max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name="количество на складе", default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    class Meta():
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


    def __str__(self):
        return f'{self.name} {self.category.name}'
