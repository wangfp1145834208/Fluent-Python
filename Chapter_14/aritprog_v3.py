import itertools

def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    ap_gen = itertools.count(begin, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
