from collections import namedtuple

class BreakException(Exception):
    pass

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        try:
            term = yield
        except BreakException:
            break
        else:
            total += term
            count += 1
            average = total/count
    return Result(count, average)

def grouper(results, key):
    while True:
        results[key] = yield from averager()

def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.throw(BreakException)

    report(results)

def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        msg = '{:3} {:5} averaging {:.2f}{}'
        print(msg.format(result.count, group, result.average, unit))

data = {
    'girls;kg':
    [40.9, 41.2, 39,7, 45.3, 40.9, 37.1, 41.8, 40.1],
    'girls;m':
    [1.52, 1.53, 1.42, 1.6, 1.47, 1.56, 1.61, 1.55, 1.51],
    'boys;kg':
    [38.2, 39, 41.2, 39.7, 39.8, 41, 37.3, 39.9],
    'boys;m':
    [1.49, 1.38, 1.51, 1.44, 1.42, 1.5, 1.39, 1.45]
}

if __name__ == '__main__':
    main(data)
