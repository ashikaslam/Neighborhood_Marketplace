from django.db import models

# Create your models here.
from user_accounts_manager.models import User

class Products(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('clothing', 'Clothing'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
        ('for_parts', 'For Parts'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='my_products',blank=True,default=None,null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    product_picture=models.ImageField(upload_to='images/product_photo',default='static_files/images/default_image.jpg',blank=True)
    email =models.CharField(max_length=100,blank=True)
    mobile_number = models.CharField(max_length=11, null=False)
    date_of_post = models.DateTimeField(auto_now=True,blank=True,null=True)
    sell_availavle=models.BooleanField(default=True)

    def __str__(self):
        return self.title
    









    
    
