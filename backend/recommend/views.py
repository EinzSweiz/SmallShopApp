from django.shortcuts import render, get_object_or_404
from shop.models import Product
from .models import Review
from .forms import ReviewForm
from django.contrib import messages
from django_htmx.http import HttpResponseClientRefresh
from django.contrib.auth.decorators import login_required

def create_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.created_by = request.user
                review.save() 
                messages.success(request, 'Review successfully added')
                return HttpResponseClientRefresh()
        else:
            messages.error(request, 'You need to be logged in to make review')
            return HttpResponseClientRefresh()

    return render(request, 'recommend/create_review.html', {'form': form, 'product': product})