from django.db import models
from django.contrib.auth.models import AbstractUser


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

    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=10 ,blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return str(self.id) + ' - ' + str(self.user) + ' => ' + str(self.total)
    

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name="order_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_product", on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    
    def __str__(self):
        return str(self.id) + ' - ' + str(self.product) + ' => ' + str(self.order)
                