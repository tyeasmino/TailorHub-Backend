from django.db import models
from fitMakers.models import FitMaker




# Create your models here.
# FabricInventoryModel ToolInventoryModel
class ToolsInventory(models.Model):
    fitmaker = models.ForeignKey(FitMaker, on_delete=models.CASCADE)   
    name = models.CharField(max_length=100)   
    stock = models.IntegerField(default=0)   
    color = models.CharField(max_length=50, blank=True, null=True)  
    category = models.CharField(max_length=100, blank=True, null=True)   
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Good', 'Good'), ('Needs Repair', 'Needs Repair')], default='Good')   
    supplier = models.CharField(max_length=100, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"
 
    def update_stock(self, quantity):
        self.stock += quantity
        self.save()



class ToolsInventoryMovement(models.Model):
    tool = models.ForeignKey(ToolsInventory, on_delete=models.CASCADE)   
    quantity = models.IntegerField()   
    movement_type = models.CharField(max_length=50, choices=[('Add', 'Add'), ('Use', 'Use')])   
    date = models.DateField(auto_now_add=True)  
    description = models.TextField(blank=True, null=True)   

    def __str__(self):
        return f"{self.movement_type} {self.quantity} {self.tool.name} on {self.date}"

 
    @staticmethod
    def create_movement(tool, quantity, movement_type, description=""):
        movement = ToolsInventoryMovement.objects.create(
            tool=tool,
            quantity=quantity,
            movement_type=movement_type,
            description=description
        ) 
        
        if movement_type == "Add":
            tool.update_stock(quantity)
        elif movement_type == "Use":
            tool.update_stock(-quantity)
        return movement






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
        # Ensure the movement type is either "Add" or "Use"
        if movement_type not in ['Add', 'Use']:
            raise ValueError("Invalid movement type. It should be 'Add' or 'Use'.")

        # Process the "Use" (sale) movement
        if movement_type == "Use":
            # Check if stock is sufficient for the "Use" movement (sale)
            if inventory_item.stock < quantity:
                raise ValueError("Not enough stock available to use.")  # Prevent creating the movement if stock is insufficient

            # Calculate the profit for the "Use" movement (sale)
            # Profit = (Sell price - Purchase price) * Quantity
            profit_per_item = inventory_item.sell_price_per_unit - inventory_item.purchase_price_per_unit
            if profit_per_item < 0:
                raise ValueError("Selling price must be greater than purchase price to make a profit.")

            total_profit = profit_per_item * quantity

            # Add the profit to the FitMaker's fabric_profit
            fitmaker.fabric_profit += total_profit

            # Calculate the total sale value (for balance update)
            total_sale_value = inventory_item.sell_price_per_unit * quantity

            # Increase the fitmaker's balance with the sale value (not decrease)
            fitmaker.balance += total_sale_value

            # After validation, decrease stock for the "Use" movement (sale)
            inventory_item.stock -= quantity

        elif movement_type == "Add":
            # Check if the FitMaker has enough balance to purchase the stock
            total_cost = inventory_item.purchase_price_per_unit * quantity
            if fitmaker.balance < total_cost:
                raise ValueError("Insufficient balance to purchase items.")

            # After validation, increase stock for the "Add" movement (purchase)
            inventory_item.stock += quantity

            # Deduct the total purchase cost from FitMaker's balance
            fitmaker.balance -= total_cost

        # Save the updated inventory item and FitMaker balance
        inventory_item.save()
        fitmaker.save()

        # Create the inventory movement record
        movement = InventoryItemMovement.objects.create(
            inventory_item=inventory_item,
            quantity=quantity,
            movement_type=movement_type,
            description=description
        )

        return movement


