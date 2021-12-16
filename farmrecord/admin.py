from django.contrib import admin
from farmrecord.models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(CowRecords)
admin.site.register(PigRecords)
admin.site.register(GoatRecords)
admin.site.register(SheepRecords)