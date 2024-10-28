from decimal import Decimal
from shop.models import ProductProxy

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        :param product: The product to add.
        :param quantity: Number of items to add.
        :param update_quantity: Boolean to indicate if the quantity should be updated.
        """
        product_id_str = str(product.id)
        discount_price = product.get_discount_price()
        # Store the discounted price as Decimal or None
        price = Decimal(product.price)
        discounted_price = discount_price if discount_price is not None else price

        if product_id_str not in self.cart:
            self.cart[product_id_str] = {
                'qty': quantity,
                'price': str(price),
                'discounted_price': str(discounted_price) if discounted_price is not None else price  # Use original price if no discount
            }
        else:
            self.cart[product_id_str]['qty'] = quantity  # Update quantity for existing item

        self.save()

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def remove(self, product_id):
        """
        Remove a product from the cart.
        :param product_id: ID of the product to remove.
        """
        product_id_str = str(product_id)
        if product_id_str in self.cart:
            del self.cart[product_id_str]
            self.save()

    def update(self, product_id, quantity):
        product_id_str = str(product_id)
        if product_id_str in self.cart:
            self.cart[product_id_str]['qty'] = quantity
            self.save()

    def save(self):
        """
        Save the cart to the session.
        """
        self.session['session_key'] = self.cart
        self.session.modified = True

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        
        :return: Total price as a Decimal.
        """
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
    
    def get_discounted_total_price(self):
        """
        Calculate the total price of all items in the cart, applying the discounted price if available.
        
        :return: Discounted total price as a Decimal.
        """
        total = Decimal('0.00')
        for item in self.cart.values():
            price = Decimal(item.get('discounted_price', item['price']))
            total += price * item['qty']
        return total

    def has_discount(self):
        """
        Check if the cart has any discounted items and if the discounted total is less than the regular total.
        """
        return self.get_discounted_total_price() < self.get_total_price()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item