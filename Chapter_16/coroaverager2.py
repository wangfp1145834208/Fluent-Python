from collections import namedtuple

Result = namedtuple('Result', 'count average')

def average():
    total = 0.0
    count = 0
    average = None
    print('Caculating the AVG...')
    while True:
        term = yield
        if term si None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)
