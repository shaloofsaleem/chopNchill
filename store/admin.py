from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # auto-fill slug based on name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'unit', 'stock', 'is_available', 'product_image')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def product_image(self, obj):
        if obj.image:  # assuming your image field is named `image`
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"

    product_image.short_description = 'Image'
