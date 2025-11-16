from django.db import models

# Create your models here.
class user(models.Model):
    usernname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)  # Optional

CATEGORY_CHOICES = (
    ("special", "Special Collection"),
    ("cord", "Cord Set Kurtis"),
    ("short", "Short Kurtis"),
    ("saree", "Saree"),
)

category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="special")



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=10, null=True, blank=True)  # e.g., S, M, L, XL
    color = models.CharField(max_length=30, null=True, blank=True)  #
    category = models.CharField(max_length=50, null=True, blank=True)  # e.g
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional offer price
    code= models.CharField(max_length=50, unique=True, null=True, blank=True)  # Unique product code
    fabric = models.CharField(max_length=100, null=True, blank=True)  # e.g., Cotton, 
    

    
class icart(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    total_price=models.IntegerField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

class Wishlist(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    

  
from django.db.models import Avg


class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    
    rating = models.PositiveIntegerField(default=5)  # 1–5 stars
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first
        unique_together = ('product', 'user')  # user can review product only once

    def __str__(self):
        return f"{self.product.title} - {self.rating}★"

    @staticmethod
    def avg_rating(product):
        return Review.objects.filter(product=product).aggregate(Avg("rating"))["rating__avg"] or 0
    



class Transaction(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    order_id= models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)