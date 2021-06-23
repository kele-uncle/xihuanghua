from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index= True)
    slug = models.SlugField(max_length = 200, db_index=True)
    class Meta:
        ordering=('name',)
        verbose_name = 'category'#nick name to use through out the startproject
        verbose_name_plural = 'categories'#also this name can be used and can be recogonozed

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name= 'products', on_delete= models.CASCADE)
    name = models.CharField(max_length= 200, db_index=True)
    slug = models.SlugField(max_length= 200, db_index=True)
    price = models.DecimalField(max_digits= 10 , decimal_places= 2)
    image = models.ImageField(upload_to= 'products/%Y/%m/%d', blank= True)#to use this upload_to install pillow app
    description = models.TextField(blank= True)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)
    availability = models.BooleanField(default = True)

    class Meta:
        ordering=('name',)
        index_together = (('id','slug'),)#this will make index jha id and slug dono ho, like id 1 nd slug = xyz on this page

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
