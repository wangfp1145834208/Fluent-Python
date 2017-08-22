from collections import namedtuple
import promotions
import inspect

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.quantity * self.price

class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __str__(self):
        fmt = '<Order total: {:.2f} due: {:.2f} promotion: {} customer: {}>'
        return fmt.format(self.total(), self.due(), self.promotion.__doc__, self.customer.name)

promos = [func for name, func in
        inspect.getmembers(promotions, inspect.isfunction)]

def best_promo(order):
    'best promotion choice'
    return max(promo(order) for promo in promos)

if __name__ == '__main__':
    song = Customer('Song Tianhang', 2050)
    cong = Customer('Cong liang', 50)
    cart = [LineItem('book', 30, 35.5),
            LineItem('phone', 2, 3000),
            LineItem('close', 17, 120),
            LineItem('shoe', 7, 210)]

    print(Order(song, cart, best_promo))
    print(Order(cong, cart, best_promo))
