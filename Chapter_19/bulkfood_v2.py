class LineItem:

    def __init__(self, description, weight, price):
        self.__description = description
        self.__weight = weight
        self.__price = price

    def subtotal(self):
        return self.__weight * self.__price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')
