from django.test import TestCase
from django.test import RequestFactory
from  .views import cart_view
from  .cart import Cart

class CartViewTest(TestCase):
    def test_renders_cart_view_template_with_context(self):

        request = RequestFactory().get('/cart/')
        cart = Cart(request)
        response = cart_view(request)

        assert response.status_code == 200
        assert 'cart/cart_view.html' in [t.name for t in response.templates]
        assert response.context_data['cart'] == cart