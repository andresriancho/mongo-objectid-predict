import operator

from .object_id import ObjectId


def predict(base, backward=False, counter_diff=20, per_counter=60):
    """
    :param base: The base object ID

    :param backward: True if we should predict object IDs which were created before the base.

    :param counter_diff: How many +1 or -1 do we want to try to brute-force in the 3-byte
                         counter?

    :param per_counter: The ObjectId has a counter which auto-increments (+1)
                        on each object creation. For each counter that we increment
                        or decrement (depending on forward parameter) this parameter
                        determines how many seconds we have to add or substract to
                        the epoch.

    :yield: Object ids
    """
    looks_like, reason = ObjectId.looks_like(base)
    if not looks_like:
        raise Exception(reason)

    base = ObjectId(base)
    oper = {False: operator.add, True: operator.sub}.get(backward)

    for counter_iter in xrange(1, counter_diff):
        for epoch_iter in xrange(per_counter):
            copy = base.copy()

            copy.counter = oper(copy.counter, counter_iter)
            copy.epoch = oper(copy.epoch, epoch_iter)

            yield str(copy)
