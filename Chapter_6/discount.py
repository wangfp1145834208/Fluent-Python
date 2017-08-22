from abc import ABC, abstractmethod
from collections import namedtuple

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
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __str__(self):
        fmt = '<Order total: {:.2f} due: {:.2f} promotion: {}>'
        return fmt.format(self.total(), self.due(), self.promotion)

class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        pass

class FidelityPromo(Promotion):
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0

    def __repr__(self):
        return 'fidelity promotion' 

class BulkItemPromo(Promotion):
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount

    def __repr__(self):
        return 'bulk item promotion'   

class LargeOrderPromo(Promotion):
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0

    def __repr__(self):
        return 'large order promotion'

if __name__ == '__main__':
    song = Customer('Song Tianhang', 2050)
    cong = Customer('Cong liang', 50)
    cart = [LineItem('book', 30, 35.5),
            LineItem('phone', 2, 3000),
            LineItem('close', 17, 120),
            LineItem('shoe', 7, 210)]
    print(Order(song, cart, FidelityPromo()))
    print(Order(cong, cart, FidelityPromo()))
    print(Order(song, cart, BulkItemPromo()))
    
    long_order = [LineItem(str(item), 1, 1.2) for item in range(12)]
    print(Order(cong, long_order, LargeOrderPromo()))
