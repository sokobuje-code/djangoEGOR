
from django.contrib import admin
from .models import Post, Book, Product

admin.site.register(Post)
admin.site.register(Book)
admin.site.register(Product)
from .models import Category

admin.site.register(Category)
