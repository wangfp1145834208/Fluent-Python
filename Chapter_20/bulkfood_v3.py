class Quantity:

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        # instance 是 LineItem 的实例
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = '{!r} must be > 0.'.format(self.storage_name)
            raise ValueError(msg)


class LineItem:
    # weight, price 既是描述符类实例，又是托管类实例
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

