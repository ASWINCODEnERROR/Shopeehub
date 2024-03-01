from django.db import models
import uuid
from  django.conf import settings
from django.db.models import Avg
from django.contrib.auth.models import User


# Create your models here.
        
class Category(models.Model):
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    slug = models.SlugField(default= None)
    featured_product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='featured_product')
    icon = models.CharField(max_length=100, default=None, blank = True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    
# Product
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount = models. BooleanField(default=False)
    old_price = models.FloatField(default=100.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    slug = models.SlugField(default=None, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    inventory = models.IntegerField(default=5)
    image = models.ImageField(upload_to = 'img',  blank = True, null=True, default='')
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    price = models.FloatField(default=100.0)
    size = models.CharField(max_length=50, blank=True, null=True) 
    color = models.CharField(max_length=50, blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # created
     
   
    @property
    def  offer_price(self):
        if self.discount:
            new_price = self.old_price -((30/100)*self.old_price)
        else:
           return self.old_price
        
    
    def __str__(self):
        return self.name
 
#for multiple images for a product 
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/',default="",null=True,blank=True)

    @property
    def img(self):
        if self.image =="":
            self.image =""
                
        return self.image
    
    def __str__(self):
        return self.name

# 
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50)
    price = models.FloatField(default=100.00)
    inventory = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
# # # clolo
    
  
    
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "reviews")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.description
    
    

class Rating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name = 'rating')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=((1,'1 star'),(2,'2 star'),(3,'3 star'),(4,'4 star'),(5,'5 star')))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product','user')
        
    @property
    def average_rating(self):
        return self.product.ratings.aggregate(Avg('rating'))['rating__avg']

    @property
    def total_ratings(self):
        return self.product.ratings.count()

    def __str__(self):
        return f"Rating for {self.product.name} by {self.user.username}"