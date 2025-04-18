# shop/context_processors.py

from .models import *  # adjust according to your actual model path

def categories_processor(request):
    categories = Category.objects.all()
    return {
        'categories': categories
    }
