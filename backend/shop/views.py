from django.shortcuts import redirect, render, get_object_or_404
from .models import ProductProxy, Category
from django.views.generic import ListView
from recommend.models import Review
from django.core.cache import cache
# def product_list_view(request):
#     qs = ProductProxy.objects.all()
#     return render(request, 'shop/products.html', {'products': qs})

class ProductListView(ListView):
    model = ProductProxy
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        cache_key = f'product_list_page_{self.request.GET.get("page", 1)}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, timeout=60*15)
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return 'shop/components/product_list.html'
        return 'shop/products.html'
    
def product_detail_view(request, slug):
    cache_key = f'product_detail_{slug}'
    product = cache.get(cache_key)
    if not product:
        product = get_object_or_404(ProductProxy, slug=slug)
        cache.set(cache_key, product, timeout=60*15)
    reviews = Review.objects.filter(product=product).select_related('created_by')
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'shop/product_detail.html', context=context)


def categories_list(request, slug):
    cache_key = f'category_{slug}'
    category = cache.get(cache_key)
    if not category:
        category = get_object_or_404(Category, slug=slug)
        cache.set(cache_key, category, timeout=60*15)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/category_list.html', context=context)


def search_products(request):
    query = request.GET.get('q')
    products = ProductProxy.objects.filter(title__icontains=query).distinct()
    context = {
        'products': products
    }
    if not query or not products or len(products) == 0:
        return redirect('product_list')
    return render(request, 'shop/products.html', context=context)