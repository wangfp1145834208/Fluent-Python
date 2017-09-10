class TestMetaClass(type):

    def __init__(cls, name, bases, dict):
        pass


class Test(metaclass=TestMetaClass):
    pass


class SubTest(Test):
    pass


class SubMeta(TestMetaClass):
    pass


if __name__ == '__main__':
    result_1 = issubclass(Test, TestMetaClass)
    print('*** Is Test the subclass of TestMetaClass?({})'.format(result_1))
    result_2 = isinstance(Test, TestMetaClass)
    print('*** Is Test the instance of TestMetaClass?({})'.format(result_2))
    print(50 * '-')
    result_3 = issubclass(SubTest, TestMetaClass)
    print('*** Is SubTest the subclass of TestMetaClass?({})'.format(result_3))
    result_4 = isinstance(SubTest, TestMetaClass)
    print('*** Is SubTest the instance of TestMetaClass?({})'.format(result_4))
    print(50 * '-')
    result_5 = issubclass(SubMeta, TestMetaClass)
    print('*** Is SubMeta the subclass of TestMetaClass?({})'.format(result_5))
    result_6 = isinstance(SubMeta, TestMetaClass)
    print('*** Is SubMeta the instance of TestMetaClass?({})'.format(result_6))

