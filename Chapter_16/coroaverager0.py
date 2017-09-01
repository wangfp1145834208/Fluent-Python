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
