from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    def __init__(self, request):#constructor
        #initializing the cart
        self.session = request.session#storing current session in a class variable so that other things within class can access it
        cart = self.session.get(settings.CART_SESSION_ID)#retreivin cart from current session
        #if cart is not there, we need to initialize a cart with an empty dictionery
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity = 1 , update_quantity= False):#update_quatity is taking to know whether we want to update or add the values
        #add a product to cart or updates its value
        product_id = str(product.id)#for latter json convertion
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price) }
        if update_quantity:
            self.cart[product_id]['quantity']= quantity
        else:
            self.cart[product_id]['quantity']+= quantity
        self.save()#to save cart in session

    def save(self):
        #mark session as modified to make sure it gets save
        self.session.modified = True

    def remove(self,product):
        #remove a product from the cart
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()#to get only keys from dictionery
        products = Product.objects.filter(id__in = product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    #remove the cart from session
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
