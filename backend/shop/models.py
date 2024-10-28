import string
from django.db import models
from django.utils.text import slugify
import random
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', blank=True, null=True
    )
    slug = models.SlugField(max_length=250, unique=True, null=False, editable=True, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])
    
    @staticmethod
    def _rand_slug():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self._rand_slug() + '-pickBetter' + self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'slug':self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, verbose_name='URL')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/products/%Y/%m/%d', default='products/products/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug':self.slug})
    
    def get_discount_price(self):
        discount_price = self.price - (self.price * self.discount / 100)
        return round(discount_price, 2)
    
    @property
    def full_image_url(self):
        return self.image.url if self.image else ''


class ProductManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(available=True)

class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True