from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True) 
    slug = models.SlugField(max_length=80)

    def __str__(self):
        return self.name
    

class FitMaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # shop name 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fabric_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.URLField(max_length=255, blank=True, null=True)

    # company details
    shop_started = models.DateField(blank=True, null=True) 
    shop_address = models.CharField(max_length=200, blank=True, null=True)
    shop_hours = models.CharField(max_length=100, blank=True, null=True)

    # contact details 
    phone = models.CharField(max_length=11, null=True, blank=True) 
    whatsapp = models.CharField(max_length=11, null=True, blank=True) 
    website = models.URLField(max_length=100, blank=True, null=True) 
    facebook = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)

    services = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.shop_address if self.shop_address else ''}"





class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name



class Dress(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    fabric_type = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    image = models.URLField(max_length=255, blank=True, null=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  
    is_on_sale = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(default=0)  
    min_stock_level = models.IntegerField(default=5) 
    is_available = models.BooleanField(default=True) 
    supplier_name = models.CharField(max_length=255, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    order_count = models.IntegerField(default=0)  
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fit_maker = models.ForeignKey(FitMaker, on_delete=models.CASCADE)
    is_best_seller = models.BooleanField(default=False)  
    is_upcoming = models.BooleanField(default=False)  
    is_featured = models.BooleanField(default=False)  
    slug = models.SlugField(max_length=255, unique=True, blank=True)


    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0  # Return 0 if no ratings exist

    def update_best_seller_status(self):
        """ Update the best seller status based on total sales or other criteria """
        if self.total_sales >= 2:  # Example: If a dress sells more than 1000 units, mark it as a best seller
            self.is_best_seller = True
        else:
            self.is_best_seller = False
        self.save()


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.name





class DressRating(models.Model): 
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, choices=[(i, i) for i in range(6)], default=0)  # 0-5 rating
    comment = models.TextField(blank=True, null=True)  # Optional: Allow users to leave comments with their rating
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.dress.name} with {self.rating}"

    class Meta:
        unique_together = ['dress', 'user']

