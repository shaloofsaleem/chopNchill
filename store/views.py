from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Category, Product  # Make sure this is correct

def ProductPage(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    products = Product.objects.all()

    selected_category = request.GET.get('category')
    max_price = request.GET.get('price')

    if selected_category:
        products = products.filter(category__id=selected_category)
    if max_price:
        try:
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'selected_category': selected_category,
        'max_price': max_price
    }
    return render(request, 'Store/MainPageProduct.html', context)


def product_detail(request, slug):
    # Get the specific product or return 404 if not found
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Get all categories with product counts
    categories = Category.objects.annotate(product_count=Count('products'))
    
    # Fetch featured products (limit to 6)
    featured_products = Product.objects.filter(featured=True, is_available=True)[:6]

    # Get related products from the same category (exclude current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]  # Limit to 4 related products

    context = {
        'product': product,
        'categories': categories,
        'featured_products': featured_products,
        'related_products': related_products,
    }

    return render(request, 'Store/ProductDetails/productDetailed.html', context)

def category_products(request, slug=None):
    categories = Category.objects.annotate(product_count=Count('products'))
    products = Product.objects.all()

    selected_category = None
    if slug:
        selected_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=selected_category)

    max_price = request.GET.get('price')
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'selected_category': selected_category,
        'max_price': max_price
    }

    return render(request, 'Store/Category/category.html', context)


