from evalsupport import deco_alpha
from evalsupport import MetaAleph

print('<[1]> evaltime_meta module start')


@deco_alpha
class ClassThree():
    print('<[2]> ClassThree body')

    def method_y(self):
        print('<[3]> ClassThree.method_y')


class ClassFour():
    print('<[4]> ClassFour body')

    def method_y(self):
        print('<[5]> ClassFour.method_y')


class ClassFive(metaclass=MetaAleph):
    print('<[6]>')

    def __init__(self):
        print('<[7]>')

    def method_z(self):
        print('<[8]>')


class ClassSix(ClassFive):
    print('<[9]>')

    def method_z(self):
        print('<[10]>')


if __name__ == '__main__':
    print('<[11]>')
    three = ClassThree()
    three.method_y()
    print('<[12]>')
    four = ClassFour()
    four.method_y()
    print('<[13]>')
    five = ClassFive()
    five.method_z()
    print('<[14]>')
    six = ClassSix()
    six.method_z()

print('<[15]>')

