from django.contrib import admin
from farmrecord.models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Section)
admin.site.register(CowMortality)
admin.site.register(PigMortality)
admin.site.register(SheepMortality)
admin.site.register(GoatMortality)
admin.site.register(CowSale)
admin.site.register(PigSale)
admin.site.register(GoatSale)
admin.site.register(SheepSale)
admin.site.register(CowProcurement)
admin.site.register(GoatProcurement)
admin.site.register(PigProcurement)
admin.site.register(SheepProcurement)
admin.site.register(CowCulling)
admin.site.register(GoatCulling)
admin.site.register(SheepCulling)
admin.site.register(PigCulling)
