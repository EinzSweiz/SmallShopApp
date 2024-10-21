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
        :param product_id: ID of the product to add.
        :param quantity: Number of items to add.
        :param update_quantity: Boolean to indicate if the quantity should be updated.
        """
        product_id_str = str(product.id)
        
        if product_id_str not in self.cart:
            self.cart[product_id_str] = {'qty': quantity, 'price': str(product.price)}
        
        # if update_quantity:
        self.cart[product_id_str]['qty'] = quantity
        # else:
        #     self.cart[product_id_str]['qty'] += quantity
        
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