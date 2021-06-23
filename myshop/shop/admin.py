from django.contrib import admin
from .models import Category,Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields={'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','availability','created','updated']
    list_filter = ['availability','created','updated']
    prepopulated_fields = {'slug':('name',)}
    list_edittable = ['price','availability']#can edit bahar se hi
