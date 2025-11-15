from django.contrib import admin
from .models import EmissionFactor, Activity, ConvertedEmission 
# Register your models here.
admin.site.register(EmissionFactor)
admin.site.register(Activity)
admin.site.register(ConvertedEmission)