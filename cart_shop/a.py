'''@login_required
class Cart(object):
    def __init__(self, request):
        self.user = request.user
        cart = self.user
        if not cart:
            cart = self.user
        self.cart = cart


    def add(self, product, quantity, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product_entry.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.user = self.cart

    def remove(self, product):
        self.product_id = str(product.id)
        if self.product_id in self.cart:
            del self.cart[self.product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()

        products = product_entry.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        
        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price'])* item ['quantity'] for item in self.cart.values())
'''