from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Crop)
admin.site.register(GardenGroup)
admin.site.register(Plant)
admin.site.register(Task)
