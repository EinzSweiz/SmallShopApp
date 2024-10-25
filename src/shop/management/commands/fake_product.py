import os
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from shop.models import Product, Category
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(28):
            product_title = fake.company()
            product_brand = fake.company()
            product_description = fake.paragraph(nb_sentences=2)
            product_price = fake.pydecimal(
                left_digits=3, right_digits=2, min_value=1, max_value=999.99
            )
            
            # Download image from picsum.photos
            image_url = f'https://picsum.photos/200/300?random={fake.random_number()}'
            image_content = requests.get(image_url).content
            image_name = f'{fake.slug()}.jpg'  # Create a filename for the image
            image_path = os.path.join(settings.MEDIA_ROOT, 'products', image_name)

            # Save the image to the media directory
            with open(image_path, 'wb') as image_file:
                image_file.write(image_content)
            
            # Create the product with the downloaded image
            product = Product(
                category=Category.objects.first(),
                title=product_title,
                brand=product_brand,
                description=product_description,
                slug=fake.slug(),
                price=product_price,
                available=True,
                image=f'products/{image_name}',  # Path relative to MEDIA_ROOT
                discount=fake.pyint(min_value=0, max_value=40)
            )
            product.save()

        self.stdout.write(f'Products in DB: {Product.objects.count()}')
