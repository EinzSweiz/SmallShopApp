from django.test import RequestFactory, Client, TestCase
from  .views import cart_view, cart_add_view, cart_delete_view
from django.urls import reverse
from shop.models import Category, ProductProxy
from django.contrib.sessions.middleware import SessionMiddleware
import json

# class CartViewTest(TestCase):
#     def test_renders_cart_view_template_with_context(self):

#         request = RequestFactory().get('/cart/')
#         cart = Cart(request)
#         response = cart_view(request)

#         assert response.status_code == 200
#         assert 'cart/cart_view.html' in [t.name for t in response.templates]
#         assert response.context_data['cart'] == cart


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart_view'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        response = cart_view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('cart_view')), 'cart/cart_view.html')


class CartAddViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('add_to_cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qyt': 2,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_add(self):
        request = self.factory
        response = cart_add_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['product'], 'Example Product')
        self.assertEqual(data['qty'], 2)

class CartDeleteViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('delete_from_cart'),{
            'action': 'post',
            'product_id': self.product.id,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_delete(self):
        request = self.factory
        response = cart_delete_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads[response.content]
        self.assertEqual(data['qty'], 0)