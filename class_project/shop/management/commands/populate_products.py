from django.core.management.base import BaseCommand
from shop.models import Product, Category
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the database with initial products'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = {
            'accessories': {
                'name': 'Accessories',
                'products': [
                    {"id": 1, "name": "Watch", "price": 99.99, "image": "watch.jpg"},
                    {"id": 2, "name": "Sunglasses", "price": 19.99, "image": "sunglasses.jpg"},
                    {"id": 3, "name": "Belt", "price": 13.99, "image": "belt.jpg"},
                    {"id": 4, "name": "Wallet", "price": 24.99, "image": "wallet.jpg"},
                    {"id": 5, "name": "Scarf", "price": 14.99, "image": "scarf.jpg"},
                    {"id": 6, "name": "Gloves", "price": 11.99, "image": "gloves.jpg"},
                ]
            },
            'clothing': {
                'name': 'Clothing',
                'products': [
                    {"id": 7, "name": "T-Shirt", "price": 15.99, "image": "tshirt.jpg"},
                    {"id": 8, "name": "Jeans", "price": 29.99, "image": "jeans.jpg"},
                    {"id": 9, "name": "Jacket", "price": 49.99, "image": "jacket.jpg"},
                    {"id": 10, "name": "Hoodie", "price": 34.99, "image": "hoodie.jpg"},
                    {"id": 11, "name": "Graphic Tee", "price": 18.99, "image": "graphic-tee.jpg"},
                ]
            },
            'headwear': {
                'name': 'Headwear',
                'products': [
                    {"id": 12, "name": "Hat", "price": 12.99, "image": "hat.jpg"},
                    {"id": 13, "name": "Sports Cap", "price": 10.99, "image": "sports-cap.jpg"},
                    {"id": 14, "name": "Beanie", "price": 9.99, "image": "beanie.jpg"},
                ]
            },
            'footwear': {
                'name': 'Footwear',
                'products': [
                    {"id": 15, "name": "Sneakers", "price": 59.99, "image": "sneakers.jpg"},
                ]
            },
            'bags': {
                'name': 'Bags',
                'products': [
                    {"id": 16, "name": "Backpack", "price": 39.99, "image": "backpack.jpg"},
                ]
            },
            'activewear': {
                'name': 'Activewear',
                'products': [
                    {"id": 17, "name": "Running Shorts", "price": 22.99, "image": "running-shorts.jpg"},
                ]
            }
        }

        # Create categories and products
        for category_slug, category_data in categories.items():
            category, created = Category.objects.get_or_create(
                slug=category_slug,
                defaults={'name': category_data['name']}
            )
            
            for product_data in category_data['products']:
                product, created = Product.objects.get_or_create(
                    id=product_data['id'],
                    defaults={
                        'name': product_data['name'],
                        'price': product_data['price'],
                        'category': category
                    }
                )
                
                # Handle image
                image_path = os.path.join('item_pictures', product_data['image'])
                if not os.path.exists(image_path):
                    image_path = os.path.join('media', 'item_pictures', product_data['image'])
                
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        product.image.save(product_data['image'], File(img_file), save=True)
                else:
                    self.stdout.write(self.style.WARNING(f'Image not found: {image_path}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated products and categories')) 