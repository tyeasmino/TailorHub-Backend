from django.contrib import admin
from .models import InventoryItem, InventoryItemMovement
 
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'item_type', 'fitmaker', 'color')
    search_fields = ('name', 'item_type', 'fitmaker__name', 'supplier')
    list_filter = ('item_type', 'fitmaker', 'category')

class InventoryItemMovementAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'quantity', 'movement_type', 'date', 'description')
    search_fields = ('inventory_item__name', 'movement_type', 'description', 'date')
    list_filter = ('movement_type', 'date')

admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(InventoryItemMovement, InventoryItemMovementAdmin)



