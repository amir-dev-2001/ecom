from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    picture_1 = models.ImageField(blank=True, null=True)
    picture_2 = models.ImageField(blank=True, null=True)
    picture_3 = models.ImageField(blank=True, null=True)
    picture_4 = models.ImageField(blank=True, null=True)
    picture_5 = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title