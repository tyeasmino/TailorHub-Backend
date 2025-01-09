from django.db import models
from fitMakers.models import FitMaker




# Create your models here.
class InventoryItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('Tool', 'Tool'),
        ('Fabric', 'Fabric'),
    ]

    fitmaker = models.ForeignKey(FitMaker, on_delete=models.CASCADE)  
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES)
    name = models.CharField(max_length=100) 
    purchase_price_per_unit=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sell_price_per_unit=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)    
    image = models.URLField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(default=0)
    color = models.CharField(max_length=50, blank=True, null=True) 
    supplier = models.CharField(max_length=100, blank=True, null=True)  
    description = models.TextField(null=True, blank=True)  
    category = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"{self.name} ({'Tool' if self.item_type == 'Tool' else 'Fabric'}) - (Stock: {self.stock})"

    

class InventoryItemMovement(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=50, choices=[('Add', 'Add'), ('Use', 'Use')])
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.movement_type} {self.quantity} {self.inventory_item.name} on {self.date}"

    @staticmethod
    def create_movement(fitmaker, inventory_item, quantity, movement_type, description=""):
        if movement_type not in ['Add', 'Use']:
            raise ValueError("Invalid movement type. It should be 'Add' or 'Use'.")

       
        if movement_type == "Use":
            if inventory_item.stock < quantity:
                raise ValueError("Not enough stock available to use.")  

            profit_per_item = inventory_item.sell_price_per_unit - inventory_item.purchase_price_per_unit
            if profit_per_item < 0:
                raise ValueError("Selling price must be greater than purchase price to make a profit.")

            total_profit = profit_per_item * quantity
            fitmaker.fabric_profit += total_profit
            total_sale_value = inventory_item.sell_price_per_unit * quantity
            fitmaker.balance += total_sale_value
            inventory_item.stock -= quantity

        elif movement_type == "Add":
            total_cost = inventory_item.purchase_price_per_unit * quantity
            if fitmaker.balance < total_cost:
                raise ValueError("Insufficient balance to purchase items.")

            inventory_item.stock += quantity
            fitmaker.balance -= total_cost

        inventory_item.save()
        fitmaker.save()

        movement = InventoryItemMovement.objects.create(
            inventory_item=inventory_item,
            quantity=quantity,
            movement_type=movement_type,
            description=description
        )

        return movement


