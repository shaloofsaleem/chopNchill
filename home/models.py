# app/models.py
from django.db import models

class HeroSection(models.Model):
    subtitle = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    input_placeholder = models.CharField(max_length=100, default="Search")
    button_text = models.CharField(max_length=50, default="Submit Now")

    def __str__(self):
        return self.title

class CarouselItem(models.Model):
    hero_section = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name="carousel_items")
    image = models.ImageField(upload_to='hero/')
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label
