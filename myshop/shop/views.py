from django.shortcuts import render,get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request, category_slug= None):
    category = None#this is the category which will be selected by customer, initially it is none
    categories = Category.objects.all()#extracting all the categories
    products = Product.objects.filter(availability = True)#extracting all available products
    if category_slug:#now if selected category is not none and customer have selected somthing
        category = get_object_or_404(Category, slug = category_slug)#to ab jo slug column of Category table mai slug_category daal do
        products = products.filter(category= category)#now us ek particular category ke products
    return render(request, 'shop/product/list.html',{"categories":categories, "products":products, "category":category})

def product_detail(request,id,slug):
    product = get_object_or_404(Product, id= id, slug= slug, availability=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',{"product":product, "cart_product_form":cart_product_form ,})
