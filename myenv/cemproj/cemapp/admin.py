from django.contrib import admin

# Register your models here.
from .models import Fertilizer
admin.site.register(Fertilizer) 
admin.site.site_header = 'CEM Admin'
admin.site.site_title = 'CEM Admin'

from .models import (
    Profile, Fertilizer, SoilType, Crop, 
)
# filepath: c:\cms\myenv\cemproj\cemapp\admin.py
from django.contrib import admin
from .models import SoilType

class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  # Removed 'ph_range'

admin.site.register(SoilType, SoilTypeAdmin)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'ideal_soil')

from django.contrib import admin
from .models import Recommendation

admin.site.register(Recommendation)
# @admin.register(FertilizerRecommendation)
# class FertilizerRecommendationAdmin(admin.ModelAdmin):
#     list_display = ('crop', 'soil_type')

