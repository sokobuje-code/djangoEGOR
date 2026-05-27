
from django.db import models
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.price is None:
            return
        if self.price <= 0:
            raise ValidationError('Цена должна быть положительной')
        if self.name and len(self.name) < 3:
            raise ValidationError('Название должно быть длиннее 3 символов')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)