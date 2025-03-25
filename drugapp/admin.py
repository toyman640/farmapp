from django.contrib import admin
from drugapp.models import *

# Register your models here.
admin.site.register(Unit)
admin.site.register(Drug)
admin.site.register(Dispatch)
admin.site.register(InventoryLog)
admin.site.register(PendingStockUpdate)
