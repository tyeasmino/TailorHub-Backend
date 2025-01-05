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





# class Fabric(models.Model):
#     fitmaker = models.ForeignKey(FitMaker, on_delete=models.CASCADE)  # Link fabric to a specific FitMaker
#     name = models.CharField(max_length=100)
#     material = models.CharField(max_length=100)
#     color = models.CharField(max_length=50)
#     price_per_meter = models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity = models.IntegerField(default=0)
#     description = models.TextField(null=True, blank=True)  # Optional additional information
    
#     def __str__(self):
#         return f"{self.name} ({self.material}) - {self.color}"