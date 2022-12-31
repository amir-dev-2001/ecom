from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=11, verbose_name='number')
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=10 ,blank=True, null=True)
    
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
    image = models.ImageField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.title    
    
    
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    
    # item = models.ManyToManyField(
    #     'Product',
    #     related_name='carts'
    # )

    # product_names = models.CharField(max_length=500)
    # item = models.ForeignKey(Pr   oduct, on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.CharField(max_length=100, default=0)
    transaction_id = models.CharField(max_length=150, default=0)
    total_amount = models.CharField(max_length=50, default=0)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return str(self.user) + ' => ' + str(self.total_amount)
    
# class OrderItem(models.Model):
        