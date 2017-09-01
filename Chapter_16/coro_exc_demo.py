class DemoException(Exception):
    pass

class BreakException(Exception):
    pass

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        except BreakException:
            break
        else:
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run.')
