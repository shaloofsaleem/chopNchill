from django.shortcuts import render
from .models import *
from store.models import *
from django.core.paginator import Paginator
from django.db.models import Q, Count

def homePage(request):
    hero = HeroSection.objects.first()
    carousel_items = CarouselItem.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    featured_products = Product.objects.filter(featured=True, is_available=True)
    best_selling_products = Product.objects.filter(best_seller=True, is_available=True)

    context = {
        'hero': hero,
        'carousel_items': carousel_items,
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
        'best_selling_products': best_selling_products,
    }
    return render(request, 'LandingPage/home.html', context)


def search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
    selected_category = request.GET.get('category')
    max_price = request.GET.get('price')

    # Categories with product counts (regardless of search)
    categories = Category.objects.annotate(product_count=Count('products'))

    # Search results with optional filters
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if selected_category:
        products = products.filter(category__id=selected_category)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'Search/product-list.html', {
        'query': query,
        'results':results,
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'max_price': max_price,
    })

def contactPage(request):
    return render(request, 'Contact/contact.html')