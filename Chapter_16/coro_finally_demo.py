class DeomException(Exception):
    pass

def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else:
            print('-> coroutine received: {!r}'.format(x))
    finally:
        print('-> coroutine ending')
