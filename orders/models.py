import string
import random
from django.db import models
from decimal import Decimal  # Make sure Decimal is imported
from fitFinders.models import FitFinder
from fitMakers.models import FitMaker
from inventory.models import InventoryItem
from measurements.models import DressType



class CartList(models.Model):
    fit_finder = models.ForeignKey(FitFinder, on_delete=models.CASCADE)
    fit_maker = models.ForeignKey(FitMaker, on_delete=models.CASCADE)   

    fabric_or_dress = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True)
    fabric_or_dress_quantity = models.PositiveIntegerField(default=1)
    tailorService = models.ForeignKey(DressType, on_delete=models.SET_NULL, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"CartItem for {self.fit_finder.user.username} - {self.fabric_or_dress.name}"

    class Meta:
        ordering = ['added_at']





ORDER_STATUS_CHOICES = [
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
    ('Delivered', 'Delivered'),
]

class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    fit_finder = models.ForeignKey(FitFinder, on_delete=models.CASCADE)
    fit_maker = models.ForeignKey(FitMaker, on_delete=models.CASCADE)

    fabric_OR_dress = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True)
    fabric_OR_dress_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fabric_OR_dress_quantity = models.PositiveIntegerField(default=1)

    tailorService = models.ForeignKey(DressType, on_delete=models.SET_NULL, null=True, blank=True)
    tailorService_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    total_bill = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Processing')

    def generate_order_id(self):
        # Ensure a random unique string is generated
        while True:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            order_id = f"ORD#{random_string}"
            # Check if the generated order_id already exists in the database
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id

    def save(self, *args, **kwargs):
        if self.fabric_OR_dress:
            if self.fabric_OR_dress.discount_price != '0.00':
                self.fabric_OR_dress_price = self.fabric_OR_dress.discount_price
            else:
                self.fabric_OR_dress_price = self.fabric_OR_dress.base_price

            # Ensure fabric_OR_dress_quantity is an integer and not an empty string
            try:
                self.fabric_OR_dress_quantity = int(self.fabric_OR_dress_quantity) if self.fabric_OR_dress_quantity != '' else 1
            except (ValueError, TypeError):
                self.fabric_OR_dress_quantity = 1  # Default to 1 if invalid

            # Safely handle the multiplication, ensuring both are of numeric types
            try:
                self.fabric_OR_dress_price = Decimal(self.fabric_OR_dress_price) * self.fabric_OR_dress_quantity
            except (TypeError, ValueError):
                self.fabric_OR_dress_price = Decimal(0)  # Default to zero if invalid

        if self.tailorService:
            # Ensure tailorService_price is a valid number and assign correctly
            self.tailorService_price = Decimal(self.tailorService.sell_price_per_unit or 0)

        # Calculate total_bill with proper defaults
        self.total_bill = (self.fabric_OR_dress_price or Decimal(0)) + (self.tailorService_price or Decimal(0))

        # If the order is being marked as completed, reduce the stock
        if self.order_status == 'Completed' and not self.pk:  # This check ensures we only update on creation
            self.update_inventory_on_complete()

        if not self.order_id:  # If the order ID is not set yet
            self.order_id = self.generate_order_id()

        super().save(*args, **kwargs)

    def update_inventory_on_complete(self):
        if self.fabric_OR_dress:
            if self.fabric_OR_dress.stock >= self.fabric_OR_dress_quantity:
                self.fabric_OR_dress.stock -= self.fabric_OR_dress_quantity  # Decrease fabric stock by 1
                self.fabric_OR_dress.save()

    def __str__(self):
        return f"{self.order_id} - {self.fit_finder.user.username}"
