from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Category, Product

# ---------------------------------------------
# 🛍️ All Products Page with Category & Price Filters
# ---------------------------------------------
def ProductPage(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    products = Product.objects.all()
    tags = ['Organic', 'Fresh', 'Sales', 'Discount', 'Expired']

    # GET parameters
    selected_category = request.GET.get('category')
    max_price = request.GET.get('price')
    search_query = request.GET.get('q')  # 'q' is the search keyword

    # Filters
    if selected_category:
        products = products.filter(category__id=selected_category)

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if search_query:
        products = products.filter(name__icontains=search_query)  # adjust field name if needed

    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'selected_category': selected_category,
        'max_price': max_price,
        'tags': tags,
        'search_query': search_query
    }
    return render(request, 'Store/MainPageProduct.html', context)

# ---------------------------------------------
# 🔍 Product Detail View
# ---------------------------------------------
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    categories = Category.objects.annotate(product_count=Count('products'))

    # Featured products (e.g., carousel)
    featured_products = Product.objects.filter(featured=True, is_available=True)[:6]

    # Related products from same category (excluding current one)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'categories': categories,
        'featured_products': featured_products,
        'related_products': related_products,
    }
    return render(request, 'Store/ProductDetails/productDetailed.html', context)

# ---------------------------------------------
# 📂 Products by Category Slug with Price Filter
# ---------------------------------------------
def category_products(request, slug=None):
    categories = Category.objects.annotate(product_count=Count('products'))
    products = Product.objects.all()
    selected_category = None
    search_query = request.GET.get('q')  # Search term

    # Filter by Category Slug
    if slug:
        selected_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=selected_category)

    # Filter by Search Term
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # Filter by Price
    max_price = request.GET.get('price')
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'selected_category': selected_category,
        'max_price': max_price,
        'search_query': search_query
    }
    return render(request, 'Store/Category/category.html', context)