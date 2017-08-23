import time
from clockdeco import clock

@clock
def snooze(seconds, nonsense='nothing'):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n<2 else n*factorial(n-1)

if __name__ == '__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123, nonsense='somthing')
    print('*' * 40, 'Calling factorial(6)')
    print('6! = ', factorial(6))
