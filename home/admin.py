# app/admin.py
from django.contrib import admin
from .models import HeroSection, CarouselItem

class CarouselItemInline(admin.TabularInline):  # You can also use StackedInline
    model = CarouselItem
    extra = 1

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    inlines = [CarouselItemInline]

@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'hero_section')
