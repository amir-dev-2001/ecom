from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.dispatch import receiver
# from django.db.models.signals import post_save


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=11, verbose_name='number')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):  
        if self.first_name or self.last_name:
            return  self.first_name + ' ' + self.last_name 
        else:
            return self.username
    
    
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    is_avaliable = models.BooleanField(default=True)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    image1 = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return self.title    
   

    
class Order(models.Model):
    user = models.ForeignKey(User, related_name="user_order", on_delete=models.CASCADE)

    total = models.CharField(max_length=50, default=0)
    address = models.TextField(default=None)
    postal_code = models.CharField(max_length=10,default=None)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return str(self.id) + ' - ' + str(self.user) + ' => ' + str(self.total)
    

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name="order_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_product", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    
    def __str__(self):
        return str(self.id) + ' - ' + str(self.product) + ' => ' + str(self.order)
                

# class OrderDetail(models.Model):
#     order = models.ForeignKey(Order, related_name="order_detail", on_delete=models.CASCADE)
#     order_items = models.ManyToManyField(OrderItem, related_name="order_items")    
    
#     def __str__(self):
#         return str(self.order.user)                

'''
class Order(models.Model):
    PENDING_STATE = "p"
    COMPLETED_STATE = "c"

    ORDER_CHOICES = ((PENDING_STATE, "pending"), (COMPLETED_STATE, "completed"))

    user = models.ForeignKey(User, related_name="order", on_delete=models.CASCADE)
    order_number = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=ORDER_CHOICES, default=PENDING_STATE
    )
    is_paid = models.BooleanField(default=False)

    address = models.TextField(default=None)
    postal_code = models.CharField(max_length=10,default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


    @staticmethod
    def create_order(buyer, order_number, address, is_paid=False):
        order = Order()
        order.buyer = buyer
        order.order_number = order_number
        order.address = address
        order.is_paid = is_paid
        order.save()
        return order
    
    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_order", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    @staticmethod
    def create_order_item(order, product, quantity, total):
        order_item = OrderItem()
        order_item.order = order
        order_item.product = product
        order_item.quantity = quantity
        order_item.total = total
        order_item.save()
        return order_item    
    
    def __str__(self):
        return str(self.product)    
    
# class Cart(models.Model):
#     user = models.OneToOneField(
#         User, related_name="user_cart", on_delete=models.CASCADE
#     )
#     total = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0, blank=True, null=True
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)    


# @receiver(post_save, sender=User)
# def create_user_cart(sender, created, instance, *args, **kwargs):
#     if created:
#         Cart.objects.create(user=instance)


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, related_name="cart_product", on_delete=models.CASCADE
#     )
#     quantity = models.IntegerField(default=1)    

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)    
'''