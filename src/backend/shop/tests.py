from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy


class ProductViewTest(TestCase):
    def test_get_products(self):

        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='Django')
        product1 = Product.objects.create(
            title = 'Product 1',
            category = category,
            image = uploaded,
            slug='product-1'
        )
        product2 = Product.objects.create(
            title = 'Product 2',
            category = category,
            image = uploaded,
            slug='product-2'
        )
        response = self.client.get(reverse('product_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product1, product2])
        self.assertContains(response, product1)
        self.assertContains(response, product2)


class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='Category 1')
        product = Product.objects.create(
            title='Product 1',
            category=category,
            slug='product-1',
            image=uploaded,
        )
        response = self.client.get(reverse('product_detail', kwargs={'slug':'product-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].slug, product.slug)

class CategoryListViewTest(TestCase):
    def setUp(self):
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = ProductProxy.objects.create(
            title='Test Product', 
            slug='test-product', 
            category=self.category,
            image=uploaded,
            )
    def test_status_code(self):
        response = self.client.get(
            reverse(
                'category_list', 
                kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('category_list', kwargs={'slug':self.category.slug})
        )
        self.assertTemplateUsed(response, 'shop/category_list.html')
    
    def test_context_data(self):
        response = self.client.get(
            reverse('category_list', kwargs={'slug':self.category.slug})
        )
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)