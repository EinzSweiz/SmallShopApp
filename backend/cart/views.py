from django.shortcuts import render, get_object_or_404
from shop.models import ProductProxy
from django.http import JsonResponse
from .cart import Cart
import logging

logger = logging.getLogger(__name__)


def cart_view(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'cart/cart_view.html', context=context)



from django.http import JsonResponse, HttpResponseBadRequest

def cart_add_view(request):
    if request.method == 'POST':
        logger.debug(f"POST data: {request.POST}")
        try:
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
        except (TypeError, ValueError):
            return HttpResponseBadRequest("Invalid product ID or quantity")

        product = get_object_or_404(ProductProxy, id=product_id)

        cart = Cart(request)
        cart.add(product=product, quantity=product_qty)

        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, 'product': product.title })
        
        return response
    else:
        return HttpResponseBadRequest("Invalid request method")


def cart_delete_view(request):
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
        except (TypeError, ValueError):
            return HttpResponseBadRequest("Invalid product ID")
        cart = Cart(request)
        cart.remove(product_id=product_id)
        cart_qty = cart.__len__()
        total_price = cart.get_total_price()
        response = JsonResponse({'qty':cart_qty, 'total':str(total_price)})
        return response
 


def cart_update_view(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
        except (TypeError, ValueError) as e:
            print(f"Error converting POST data: {e}")
            return HttpResponseBadRequest("Invalid product ID or quantity")
        
        cart.update(product_id=product_id, quantity=product_qty)
            
        cart_qty = cart.__len__()
        total_price = cart.get_total_price()
        
        response = JsonResponse({'qty': cart_qty, 'total': str(total_price)})
        return response
    else:
        return HttpResponseBadRequest("Invalid request method")





