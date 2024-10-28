from django.shortcuts import redirect, render, get_object_or_404
from .models import ProductProxy, Category
from django.views.generic import ListView
from recommend.models import Review
# def product_list_view(request):
#     qs = ProductProxy.objects.all()
#     return render(request, 'shop/products.html', {'products': qs})

class ProductListView(ListView):
    model = ProductProxy
    context_object_name = 'products'
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            return 'shop/components/product_list.html'
        return 'shop/products.html'

def product_detail_view(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    reviews = Review.objects.filter(product=product).select_related('created_by')
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'shop/product_detail.html', context=context)


def categories_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
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