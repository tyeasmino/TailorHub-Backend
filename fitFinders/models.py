from django.db import models
from django.contrib.auth.models import User
from fitMakers.models import FitMaker

# Create your models here.
class FitFinder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # shop name 
    image = models.URLField(max_length=255, blank=True, null=True)

     # address details
    address = models.CharField(max_length=255, blank=True, null=True)
    preferred_fitMaker = models.ForeignKey(FitMaker, null=True, blank=True, on_delete=models.SET_NULL)

    # contact details 
    phone = models.CharField(max_length=11, null=True, blank=True) 
    whatsapp = models.CharField(max_length=11, null=True, blank=True)  
    facebook = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
