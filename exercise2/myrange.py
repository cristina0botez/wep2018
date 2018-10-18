def myrange2(start_or_end, end=None, step=1):
    if end is None:
        start = 0
        end = start_or_end
    else:
        start = start_or_end
    if step == 0:
        raise ValueError('step argument must not be 0')
    result = []
    e = start
    while (step > 0 and e < end) or (step < 0 and e > end):
        result.append(e)
        e += step
    return result


def myrange3(start_or_end, end=None, step=1):
    if end is None:
        start = 0
        end = start_or_end
    else:
        start = start_or_end
    if step == 0:
        raise ValueError('step argument must not be 0')
    e = start
    while (step > 0 and e < end) or (step < 0 and e > end):
        yield e
        e += step
