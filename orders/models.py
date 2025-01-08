import string
import random
from django.db import models
from fitFinders.models import FitFinder
from fitMakers.models import FitMaker
from inventory.models import InventoryItem
from measurements.models import DressType

# Create your models here.
ORDER_STATUS_CHOICES = [
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
    ('Delivered', 'Delivered'),
]

class Order(models.Model): 
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    fit_finder = models.ForeignKey(FitFinder, on_delete=models.CASCADE)
    fit_maker = models.ForeignKey(FitMaker, on_delete=models.CASCADE)
    
    fabric = models.ForeignKey(InventoryItem, related_name="fabric_orders", on_delete=models.SET_NULL, null=True, blank=True)
    dress = models.ForeignKey(DressType, related_name="dress_orders", on_delete=models.SET_NULL, null=True, blank=True)
    
    fabric_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dress_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def generate_order_id(self):
        """ Generate a custom, random order ID in the format `ORD-XXXXXX` """
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"ORD#{random_string.upper()}"

    def save(self, *args, **kwargs):
        # Automatically calculate the total bill if fabric and dress are selected
        if self.fabric and self.dress:
            self.fabric_price = self.fabric.sell_price_per_unit
            self.dress_price = self.dress.sell_price_per_unit
            self.total_bill = (self.fabric_price + self.dress_price)  # No discount yet

        # If the order is being marked as completed, reduce the stock
        if self.order_status == 'Completed' and not self.pk:  # This check ensures we only update on creation
            self.update_inventory_on_complete()

        if not self.order_id:  # If the order ID is not set yet
            self.order_id = self.generate_order_id()

        super().save(*args, **kwargs)

    def update_inventory_on_complete(self):
        """ Decreases the stock of the fabric and dress once the order is completed """
        if self.fabric and self.dress:
            if self.fabric.stock > 0:
                self.fabric.stock -= 1  # Decrease fabric stock by 1
                self.fabric.save()

            if self.dress.stock > 0:
                self.dress.stock -= 1  # Decrease dress stock by 1
                self.dress.save()

    def __str__(self):
        return f"{self.order_id} - {self.fit_finder.user.username}"
    


