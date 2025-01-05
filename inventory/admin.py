from django.contrib import admin
from .models import ToolsInventory, ToolsInventoryMovement
 
class ToolsInventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'category', 'color', 'condition', 'supplier')
    search_fields = ('name', 'category', 'supplier')
    list_filter = ('category', 'condition', 'supplier')
 
class ToolsInventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('tool', 'quantity', 'movement_type', 'date', 'description')
    search_fields = ('tool__name', 'movement_type', 'description', 'date')
    list_filter = ('movement_type', 'date')


admin.site.register(ToolsInventory, ToolsInventoryAdmin)
admin.site.register(ToolsInventoryMovement, ToolsInventoryMovementAdmin)
