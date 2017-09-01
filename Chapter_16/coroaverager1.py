from functools import wraps

def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen) # 预激协程
        return gen
    return primer

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    print('calculate the AVG:')
    while 1:
        term = yield average
        total += term
        count += 1
        average = total/count
