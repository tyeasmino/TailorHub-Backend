from django.db import models
from fitFinders.models import FitFinder

# Create your models here.
# DressType Model
class DressType(models.Model):
    name = models.CharField(max_length=50)   
    sell_price_per_unit=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)    
    slug = models.SlugField(max_length=60)
    icon = models.CharField(max_length=20, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# DressMeasurement Model
class DressMeasurement(models.Model):
    dress_type = models.ForeignKey(DressType, on_delete=models.CASCADE)
    fit_finder = models.ForeignKey(FitFinder, on_delete=models.CASCADE)  # Added fit_finder field
    dress_long = models.IntegerField()  # Length of the dress
    chest_or_hip = models.IntegerField()  # Chest for shirt or Hip for pant
    hand_pocket_length = models.IntegerField(null=True, blank=True)  # Sleeve length or pant's pocket length
    hand_pant_start = models.IntegerField(null=True, blank=True)  # Start point of sleeve/pant
    hand_pant_end = models.IntegerField(null=True, blank=True)  # End point of sleeve/pant
    neckband = models.IntegerField(null=True, blank=True)  # Neckband measurement (only for shirt/kamiz)

    def __str__(self):
        return f"{self.dress_type.name} Measurements for {self.fit_finder.user}"

    def is_valid_for_dress_type(self):
        if self.dress_type.name == "Shirt":
            if not all([self.dress_long, self.chest_or_hip, self.hand_pocket_length, self.hand_pant_start, self.hand_pant_end, self.neckband]):
                return False
        elif self.dress_type.name == "Pant":
            if not all([self.dress_long, self.chest_or_hip, self.hand_pant_start, self.hand_pant_end]):
                return False
        elif self.dress_type.name == "Kamiz":
            if not all([self.dress_long, self.chest_or_hip, self.hand_pocket_length, self.hand_pant_start, self.hand_pant_end, self.neckband]):
                return False
        elif self.dress_type.name == "Selowar":
            if not all([self.dress_long, self.chest_or_hip, self.hand_pant_start, self.hand_pant_end]):
                return False
        return True



